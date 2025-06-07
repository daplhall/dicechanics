import operator as op
from typing import Generator
from itertools import product, combinations
from math import sqrt
from collections import defaultdict

import DiceStatistics as ds
from DiceStatistics._inpt_cleaning import collect_faces, expand_dice, sort_dict
from DiceStatistics.types import primitives
from DiceStatistics._math import gcd

type Dice = Dice
type Pool = ds.Pool

def convert_to_dice(inpt):
	if isinstance(inpt, primitives):
		return Dice([inpt])
	elif isinstance(inpt, Dice):
		return inpt
	else:
		raise ValueError("Inpt is not a primitive or a Dice")

class Dice(object):

	def __init__(self, faces, /, mask=None, rounding=lambda x: x):
		self._data = collect_faces(faces)
		self._derived_attr()
		self._mask = mask
		self._rounding = rounding

	@classmethod
	def from_dict(cls, data: dict, mask=None, rounding=lambda x: x):
		self = cls.__new__(cls)
		self._data = sort_dict(data)
		self._derived_attr()
		self._mask = mask
		self._rounding = rounding
		return self

	def _derived_attr(self):
		self._simplify()
		self._units = sum(self._data.values())
		self._p = [i/self._units for i in self.c]
		self._mean = sum(p*f for p, f in zip(self.p, self.f))
		self._var = sum(p*(x-self._mean)**2 for x, p in zip(self.f, self.p))
		self._hash = hash(tuple(self._data.items()) + (self._mean,))
		self._cdf = self._cumulative()
		self._max = max(self._data)

	def _cumulative(self) -> list:
		res = []
		for p in self.p:  # can fold this out an call with iter to clean up the if statement
			res.append(p + res[-1] if res else p)
		return res

	def _simplify(self):
		c = self.c
		if len(c) > 1:
			d = gcd(c[0], c[1])
			for i in c[2:]:
				d = gcd(d, i)
				if d == 1:
					break
			self._data = {f: c//d for f, c in self.items()}

	@property
	def f(self) -> list:
		return list(self._data.keys())

	@property
	def p(self) -> list:
		return self._p

	@property
	def c(self) -> list:
		return list(self._data.values())

	@property
	def mean(self) -> float:
		return self._mean

	@property
	def cdf(self) -> list:
		return self._cdf

	@property
	def var(self) -> float:
		return self._var

	@property
	def std(self) -> float:
		return sqrt(self._var)

	def max(self) -> float | int:
		return self._max

	def copy(self) -> Dice:
		return Dice.from_dict(self._data)

	def max(self):
		return max(self._data.keys())

	def min(self):
		return min(self._data.keys())

	def keys(self):
		return self._data.keys()

	def values(self):
		return self._data.values()

	def items(self):
		return self._data.items()

	def reroll(self, *redo, depth: int = 1) -> Dice:
		if depth == 'inf':
			# TODO this sould just produce 0 for the face, not remove it
			return Dice(i for i in self if i not in redo)
		faces = self._data
		for _ in range(depth):
			numbers = {f: c for f, c in faces.items() if f not in redo}
			dice = {
				self: sum(c for f, c in faces.items()
						  if f in redo)
			}
			faces = expand_dice(numbers | dice)
		return Dice.from_dict(sort_dict(faces))

	def explode(self, *exploder, depth: int = 1) -> Dice:
		faces = self._data
		# redo needs to be updated, so every combination of redo adds another.
		if depth > 0:
			numbers = {
				f: c for f, c in faces.items()
				if f not in exploder
			}
			dice = {
				(self.explode(*exploder, depth=depth-1)+f): c
				for f, c in faces.items() if f in exploder
			}
			faces = expand_dice(numbers | dice)
		return Dice.from_dict(sort_dict(faces))

	def count(self, *count) -> Dice:
		return Dice(i in count for i in self)

	def equal(self, rhs) -> bool:
		if not isinstance(rhs, Dice):
			return False
		else:
			return self._hash == rhs._hash

	def folding(self, rhs, ops: callable, into) -> Dice:
		data = defaultdict(
			int,
			{f: c for f, c in self.items() if not ops(f, rhs)}
		)
		c = sum(c for f, c in self.items() if ops(f, rhs))
		data[into] += c
		return Dice.from_dict(data)

	def fold_over(self, rhs, /, into=None) -> Dice:
		return self.folding(
			rhs,
			op.gt,
			into=rhs if into is None else into
		)

	def fold_under(self, rhs, /, into=None) -> Dice:
		return self.folding(
			rhs,
			op.lt,
			into=rhs if into is None else into
		)

	def __hash__(self):
		return self._hash

	def __call__(self, func):
		def wrapper():
			self.__init__(func(i) for i in self)
			return self
		return wrapper

	def __iter__(self) -> Generator:  # might need ot be text also when mask
		for f, c in self.items():
			for _ in range(c):
				yield f

	def __contains__(self, value: any) -> bool:
		return value in self._data.keys()

	def _binary_level0(self, rhs: int | float, ops: callable) -> Dice:
		data: defaultdict[int] = defaultdict(int)
		for f, c in self.items():
			key = self._rounding(ops(f, rhs))
			data[key] += c
		return Dice.from_dict(data)

	def _binary_level1(self, rhs: Dice, ops: callable) -> Pool:
		# add "condenser" here [condesner is new word for what collects faces]
		data: defaultdict[int] = defaultdict(int)
		for ((f1, c1), (f2, c2)) in product(self.items(), rhs.items()):
			key = self._rounding(ops(f1, f2))
			data[key] += c1*c2
		return Dice.from_dict(data)

	def _binary_op(self, rhs: int | float | Dice, ops: callable) -> Dice:
		rhs = convert_to_dice(rhs)
		if isinstance(rhs, Dice):
			return self._binary_level1(rhs, ops)
		else:  # TODO This here should test the other way around. maybe have a try catch
			raise Exception("Unexpected type in dice level 0")

	def __add__(self, rhs: int | float | Dice) -> Dice:
		"""
		only does level 0, if higher up we reverse the call.
		TODO rounding reaction
		"""
		return self._binary_op(rhs, op.add)

	def __radd__(self, lhs: int | float | Dice) -> Dice:
		return self._binary_op(lhs, op.add)

	def __sub__(self, rhs: int | float | Dice) -> Dice:
		# needs to react to rounding
		return self._binary_op(rhs, op.sub)

	def __rsub__(self, lhs: int | float | Dice) -> Dice:
		return (-self)._binary_op(lhs, op.add)

	def __mul__(self, rhs: int | float | Dice) -> Dice:
		# Needs to react to rounding
		return self._binary_op(rhs, op.mul)

	def __rmul__(self, lhs: int | float | Dice) -> Dice:
		return self._binary_op(lhs, op.mul)

	def __truediv__(self, rhs: int | float | Dice) -> Dice:
		# needs to reach to rounding
		return self._binary_op(rhs, op.truediv)

	def __floordiv__(self, rhs: int | float | Dice) -> Dice:
		# needs to reach to rounding
		return self._binary_op(rhs, op.floordiv)

	def __lt__(self, rhs: int | float | Dice) -> Dice:
		return self._binary_op(rhs, op.lt)

	def __le__(self, rhs: int | float | Dice) -> Dice:
		return self._binary_op(rhs, op.le)

	def __ge__(self, rhs: int | float | Dice) -> Dice:
		return self._binary_op(rhs, op.ge)

	def __gt__(self, rhs: int | float | Dice) -> Dice:
		return self._binary_op(rhs, op.gt)

	def __eq__(self, rhs: int | float | Dice) -> Dice:
		# TODO write this and __ne__ as a general operation, also optimize
		return ds.BooleanDice.from_dice(
			self._binary_op(rhs, op.eq),  # TODO THIS IS A PERFORMANCE HOG
			self.equal(rhs)
		)

	def __ne__(self, rhs: int | float | Dice) -> Dice:
		return ds.BooleanDice.from_dice(
			self._binary_op(rhs, op.ne),  # TODO THIS IS A PERFORMANCE HOG
			not self.equal(rhs)
		)

	def _rmatmul_level0(self, lhs: int, ops: callable) -> Dice:
		if neg := lhs < 0:
			lhs *= -1
		res = self
		for _ in range(lhs-1):
			res = ops(res, self)
		return -res if neg else res

	def _rmatmul_level1(self, lhs: Dice, ops: callable) -> Dice:
		"""
		This is a overlap operations, ie overlapping 2 results
		its not the same as "adding" two dice together and thus
		the counts needs to be the same units 	
		"""
		res = []
		units = self._units
		nrolls = max(lhs.min(), lhs.max())
		for i in lhs:
			base = units**(nrolls-i)
			res += [j for j in i@self]*base
		return Dice(res)

	def _binary_rmatmul(self, lhs: int | Dice, ops: callable):
		if isinstance(lhs, int):
			return self._rmatmul_level0(lhs, ops)
		elif isinstance(lhs, Dice):
			return self._rmatmul_level1(lhs, ops)
		else:
			raise Exception("Unexpected type in dice matmul")

	def __rmatmul__(self, lhs: int | Dice) -> Dice:
		"""
				Rolls self LHS times and adds them together
		"""
		return self._binary_rmatmul(lhs, op.add)

	def __matmul__(self, rhs):
		return rhs._binary_rmatmul(self, op.add)

	def _unary_level0(self, ops: callable) -> Dice:
		return Dice(self._rounding(ops(i)) for i in self)

	def __neg__(self) -> Dice:
		return self._unary_level0(op.neg)

	def __pos__(self) -> Dice:
		return self._unary_level0(op.pos)

	def __getitem__(self, i):
		return self._data[i]

	def __repr__(self):
		return "Dice{"+str(self._data)+'}'

	def __str__(self):
		return self.__repr__()

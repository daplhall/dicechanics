import operator as op
from collections import defaultdict
from collections.abc import KeysView,ValuesView, ItemsView
from itertools import product
from math import sqrt
from typing import Generator, Callable, Iterable, Any

from dicechanics._inpt_cleaning import collect_faces, expand_dice, sort_dict
from dicechanics._math import gcd
from dicechanics.typing import BinaryFunc_T, CompareFunc_T, UnaryFunc_T

type Die_T = Die
type BooleanDie_T = BooleanDie
type PureFunc_T = Callable[[Any], Any]

PRIMITIVES = (float, int)

def convert_to_dice(inpt:object) -> Die_T:
	if isinstance(inpt, PRIMITIVES):
		return Die([inpt])
	elif isinstance(inpt, Die):
		return inpt
	else:
		raise ValueError("Inpt is not a primitive or a Die")

class Die():
	def __init__(self, faces: Iterable[float], /, rounding: PureFunc_T =lambda x: x):
		self._data = collect_faces(faces)
		self._derived_attr()
		self._rounding = rounding

	@classmethod
	def from_dict(cls, data: dict[object, int], rounding=lambda x: x) -> Die_T:
		self = cls.__new__(cls)
		self._data = sort_dict(data)
		self._derived_attr()
		self._rounding = rounding
		return self

	def _derived_attr(self):
		self._simplify()
		self._units = sum(self._data.values())
		self._p = [i / self._units for i in self.c]
		self._mean = sum(p * f for p, f in zip(self.p, self.f))
		self._var = sum(
			p * (x - self._mean) ** 2
			for x, p in zip(self.f, self.p)
		)
		self._hash = hash(tuple(self._data.items()) + (self._mean,))
		self._cdf = self._cumulative()
		self._max = max(self._data)
		self._min = min(self._data)

	def _cumulative(self) -> list[float]:
		out:list[float] = []
		for p in self.p:  # can fold this out an call with iter to clean up the if statement
			out.append(p + out[-1] if out else p)
		return out

	def _simplify(self):
		c = self.c
		if len(c) > 1:
			d = gcd(c[0], c[1])
			for i in c[2:]:
				d = gcd(d, i)
				if d == 1:
					break
			self._data = {f: c // d for f, c in self.items()}

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

	def max(self) -> float:
		return self._max

	def min(self) -> float:
		return self._min

	def copy(self) -> Die_T:
		return Die.from_dict(self._data)

	def keys(self) -> KeysView:
		return self._data.keys()

	def values(self) -> ValuesView:
		return self._data.values()

	def items(self) -> ItemsView:
		return self._data.items()

	def reroll(self, *redo, depth: int = 1) -> Die_T:
		if depth == "inf":
			# TODO this sould just produce 0 for the face, not remove it
			return Die(i for i in self if i not in redo)
		faces = self._data
		for _ in range(depth):
			numbers = {
				f: c for f, c in faces.items() if f not in redo
			}
			dice = {
				self: sum(
					c for f, c in faces.items() if f in redo
				)
			}
			faces = expand_dice(numbers | dice)
		return Die.from_dict(sort_dict(faces))

	def explode(self, *exploder, depth: int = 1) -> Die_T:
		faces = self._data
		# redo needs to be updated, so every combination of redo adds another.
		if depth > 0:
			numbers = {
				f: c
				for f, c in faces.items()
				if f not in exploder
			}
			dice = {
				(
					self.explode(*exploder, depth=depth - 1)
					+ f
				): c
				for f, c in faces.items()
				if f in exploder
			}
			faces = expand_dice(numbers | dice)
		return Die.from_dict(sort_dict(faces))

	def count(self, *count) -> Die_T:
		return Die(i in count for i in self)

	def equal(self, rhs) -> bool:
		if not isinstance(rhs, Die):
			return False
		else:
			return self._hash == rhs._hash

	def folding(self, rhs: object, ops: CompareFunc_T, into:object) -> Die_T:
		data = defaultdict(
			int, {f: c for f, c in self.items() if not ops(f, rhs)}
		)
		c = sum(c for f, c in self.items() if ops(f, rhs))
		data[into] += c
		return Die.from_dict(data)

	def fold_over(self, rhs:object, /, into:object=None) -> Die_T:
		return self.folding(
			rhs, op.gt, into=rhs if into is None else into
		)

	def fold_under(self, rhs:object, /, into:object=None) -> Die_T:
		return self.folding(
			rhs, op.lt, into=rhs if into is None else into
		)

	def perform(self, func: PureFunc_T)->Die_T:
		res = Die(func(i) for i in self)
		return res

	def __hash__(self)->int:
		return self._hash

	def __call__(self, func: PureFunc_T) -> Callable:
		def wrapper():
			return self.perform(func)
		return wrapper

	def __iter__(self) -> Generator:  # might need ot be text also when mask
		for f, c in self.items():
			for _ in range(c):
				yield f

	def __contains__(self, value: object) -> bool:
		return value in self._data.keys()

	def _binary_level0(self, rhs: object, ops: BinaryFunc_T):
		data = defaultdict[object,int](int)
		for f, c in self.items():
			key = self._rounding(ops(f, rhs))
			data[key] += c
		return Die.from_dict(data)

	def _binary_level1(self, rhs: Die_T, ops: BinaryFunc_T):
		# add "condenser" here [condesner is new word for what collects faces]
		data = defaultdict[object, int](int)
		for (f1, c1), (f2, c2) in product(self.items(), rhs.items()):
			key = self._rounding(ops(f1, f2))
			data[key] += c1 * c2
		return Die.from_dict(data)

	def _binary_op(self, rhs: object, ops: BinaryFunc_T):
		if isinstance(rhs, Die):
			return self._binary_level1(rhs, ops)
		else:
			return self._binary_level0(rhs, ops)

	def __add__(self, rhs: object) -> Die_T:
		"""
		only does level 0, if higher up we reverse the call.
		TODO rounding reaction
		"""
		return self._binary_op(rhs, op.add)

	def __radd__(self, lhs: object) -> Die_T:
		return self._binary_op(lhs, op.add)

	def __sub__(self, rhs: object) -> Die_T:
		# needs to react to rounding
		return self._binary_op(rhs, op.sub)

	def __rsub__(self, lhs: object) -> Die_T:
		return (-self)._binary_op(lhs, op.add)

	def __mul__(self, rhs: object) -> Die_T:
		# Needs to react to rounding
		return self._binary_op(rhs, op.mul)

	def __rmul__(self, lhs: object) -> Die_T:
		return self._binary_op(lhs, op.mul)

	def __truediv__(self, rhs: object) -> Die_T:
		# needs to reach to rounding
		return self._binary_op(rhs, op.truediv)

	def __floordiv__(self, rhs: object) -> Die_T:
		# needs to reach to rounding
		return self._binary_op(rhs, op.floordiv)

	def __lt__(self, rhs: object) -> Die_T:
		return self._binary_op(rhs, op.lt)

	def __le__(self, rhs: object) -> Die_T:
		return self._binary_op(rhs, op.le)

	def __ge__(self, rhs: object) -> Die_T:
		return self._binary_op(rhs, op.ge)

	def __gt__(self, rhs: object) -> Die_T:
		return self._binary_op(rhs, op.gt)

	def __eq__(self, rhs: object) -> BooleanDie_T: # type: ignore
		# TODO write this and __ne__ as a general operation, also optimize
		return BooleanDie.from_dice(
			self._binary_op(
				rhs, op.eq
			),  # TODO THIS IS A PERFORMANCE HOG
			self.equal(rhs),
		)

	def __ne__(self, rhs: object) -> BooleanDie_T: #type: ignore
		return BooleanDie.from_dice(
			self._binary_op(
				rhs, op.ne
			),  # TODO THIS IS A PERFORMANCE HOG
			not self.equal(rhs),
		)

	def _rmatmul_level0(self, lhs: int, ops: BinaryFunc_T) -> Die_T:
		if neg := lhs < 0:
			lhs *= -1
		res = self
		for _ in range(lhs - 1):
			res = ops(res, self)
		return -res if neg else res

	def _rmatmul_level1(self, lhs: Die_T, ops: BinaryFunc_T) -> Die_T:
		"""
		This is a overlap operations, ie overlapping 2 results
		its not the same as "adding" two dice together and thus
		the counts needs to be the same units
		"""
		res = []
		units = self._units
		nrolls = max(lhs.min(), lhs.max())
		for i in lhs:
			base = units ** (nrolls - i)
			res += [j for j in i @ self] * base
		return Die(res)

	def _binary_rmatmul(self, lhs: int, ops: BinaryFunc_T) -> Die_T:
		if isinstance(lhs, int):
			return self._rmatmul_level0(lhs, ops)
		elif isinstance(lhs, Die):
			return self._rmatmul_level1(lhs, ops)
		else:
			raise Exception("Unexpected type in dice matmul")

	def __rmatmul__(self, lhs: int) -> Die_T:
		"""
		Rolls self LHS times and adds them together
		"""
		return self._binary_rmatmul(lhs, op.add)

	def __matmul__(self, rhs) -> Die_T:
		return rhs._binary_rmatmul(self, op.add)

	def _unary_level0(self, ops: UnaryFunc_T) -> Die_T:
		return Die(self._rounding(ops(i)) for i in self)

	def __neg__(self) -> Die_T:
		return self._unary_level0(op.neg)

	def __pos__(self) -> Die_T:
		return self._unary_level0(op.pos)

	def __getitem__(self, i) -> Die_T:
		return self._data[i]

	def __repr__(self) -> str:
		return "Die(" + str(self._data) + ")"

	def __str__(self) -> str:
		return self.__repr__()

class BooleanDie(Die):
	def __init__(self, faces, truth: bool):
		super().__init__(faces)
		self._truth = truth
		
	@classmethod
	def from_dice(cls, dice:Die, truth: bool) -> BooleanDie_T:
		self = cls.__new__(cls)
		self._data = dice._data
		self._rounding = dice._rounding
		self._truth = truth
		self._derived_attr()
		return self
		
	def __bool__(self) -> bool:
		return self._truth
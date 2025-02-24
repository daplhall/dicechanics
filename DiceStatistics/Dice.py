from typing import Generator
from itertools import product
from math import sqrt
import operator as op
from DiceStatistics._parser import faces_to_prop
from DiceStatistics.types import primitives
from DiceStatistics._math import gcd
import DiceStatistics.Pool as Pool 

type Dice = Dice
type Pool = Pool.Pool


class Dice(object):

	def __init__(self, faces, /, mask = None, rounding = None):
		self._f, self._p, self._c, self._units = faces_to_prop(faces)		
		self._simplify()
		self._derived_attr()
		self._mask = mask if mask else None
		# TODO  make it so we just pass our floor and ceil functions instead of this
		self._rounding = rounding if rounding else lambda x: x

	def _derived_attr(self):
		self._mean = sum(p*f for p, f in zip(self.c, self.p))
		self._var = sum(p*(x-self._mean)**2 for x, p in zip(self._f, self._p))
		self._cdf = self._cumulative()

	def _cumulative(self) -> list:
		res = []
		for p in self.p: ## can fold this out an call with iter to clean up the if statement
			res.append(p + res[-1] if res else p)
		return res
		
	def _simplify(self):
		if (c := self._c) and (len(c) > 1): 
			r = gcd(c[0], c[1])
			for i in c[2:]:
				r = gcd(r, i)
			self._c = [c//r for c in self._c]

	@property
	def f(self) -> list:
		return self._f
	@property
	def p(self) -> list:
		return self._p

	@property
	def c(self) -> list:
		return self._c
	
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

	def copy(self) -> Dice:
		return Dice(i for i in self)

	def max(self):
		return max(self._f)

	def min(self):
		return min(self._f)
	
	def __iter__(self) -> Generator[int | float]: # might need ot be text also when mask
		for f, c in zip(self.f, self.c):
			for _ in range(c):
				yield f
				
	def __contains__(self, value: any) -> bool:
		return value in self._f
	
	def _binary_level0(self, rhs: int | float, ops: callable ) -> Dice:
		return Dice(self._rounding(ops(f, rhs)) for f in self)

	def _binary_level1(self, rhs: Dice, ops:callable) -> Pool:
		return Dice(self._rounding(ops(*i)) for i in product(self, rhs))
	
	def _binary_op(self, rhs: int | float | Dice, ops:callable) -> Dice:
		if isinstance(rhs, primitives):
			return self._binary_level0(rhs, ops)
		elif isinstance(rhs, Dice):
			return self._binary_level1(rhs, ops)
		else: # TODO This here should test the other way around. maybe have a try catch
			raise Exception("Unexpected type in dice level 0")

	def __add__(self, rhs: int | float | Dice | Pool) -> Dice | Pool:
		"""
		only does level 0, if higher up we reverse the call.
		TODO rounding reaction
		"""
		return self._binary_op(rhs, op.add)
	
	def __sub__(self, rhs: int | float | Dice | Pool) -> Dice | Pool:
		# needs to react to rounding
		return self._binary_op(rhs, op.sub)

	def __mul__(self, rhs: int | float | Dice | Pool) -> Dice | Pool:
		## Needs to react to rounding
		return self._binary_op(rhs, op.mul)

	def __truediv__(self, rhs: int | float | Dice | Pool) -> Dice | Pool:
		# needs to reach to rounding
		return self._binary_op(rhs, op.truediv)

	def __lt__(self, rhs: int | float | Dice) -> Dice:
		return self._binary_op(rhs, op.lt)

	def __le__(self, rhs: int | float | Dice) -> Dice:
		return self._binary_op(rhs, op.le)

	def __ne__(self, rhs: int | float | Dice) -> Dice:
		return self._binary_op(rhs, op.ne)

	def __ge__(self, rhs: int | float | Dice) -> Dice:
		return self._binary_op(rhs, op.ge)
	
	def __gt__(self, rhs: int | float | Dice) -> Dice:
		return self._binary_op(rhs, op.gt)

	def __eq__(self, rhs: int | float | Dice) -> Dice:
		return self._binary_op(rhs, op.eq)
	
	def _rmatmul_level0(self, lhs:int, ops: callable) -> Dice:
		if neg := lhs < 0:
			lhs *= -1
		res = self
		for _ in range(lhs-1):
			res = ops(res,self)
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
	
	def _binary_rmatmul(self, lhs: int | Dice, ops:callable):
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

	def _unary_level0(self, ops:callable) -> Dice:
		return Dice(self._rounding(ops(i)) for i in self)

	def __neg__(self) -> Dice:
		return self._unary_level0(op.neg)
	
	def __pos__(self) -> Dice:
		return self._unary_level0(op.pos)
	
	def __invert__(self) -> Dice:
		return self._unary_level0(op.invert)
	

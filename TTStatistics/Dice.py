from typing import Generator
from itertools import product
import operator as op
from TTStatistics._parser import faces_to_prop
from TTStatistics.types import primitives
from TTStatistics._math import ceildiv, ceil, floor, GCD
import TTStatistics.Pool as Pool 

type Dice = Dice
type Pool = Pool.Pool


class Dice(object):

	def __init__(self, faces, /, mask = None, rounding = None):
		self._f, self._p, self._c = faces_to_prop(faces)		
		self._derived_attr()
		self._mask = mask if mask else None
		# TODO  make it so we just pass our floor and ceil functions instead of this
		self._rounding = rounding if rounding else lambda x: x

	def _derived_attr(self):
		self._mean = sum([p*f for p, f in zip(self.c, self.p)])
		self._cdf = self._cumulative()

	def _cumulative(self) -> list:
		res = []
		for p in self.p: ## can fold this out an call with iter to clean up the if statement
			if res:
				res.append(p + res[-1])
			else:
				res.append(p)
		return res
		
	def _simplify(self):
		"""
			Should not be used, for it reduced (2,2,2,2,4,6)to (1,1,1,1,2,3)
			which is a wrong representation of the dice
		"""
		if (c := self._c) and (len(c) > 1): 
			r = GCD(c[0], c[1])
			for i in c[2:]:
				r = GCD(r, i)
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

	def copy(self) -> Dice:
		copy = Dice(i for i in self)
		return copy


	def __iter__(self) -> Generator[int | float]: # might need ot be text also when mask
		for f, c in zip(self.f, self.c):
			for _ in range(c):
				yield f
				
	def __contains__(self, value: any) -> bool:
		return value in self._f
	
	#TODO experiment with this just generating the faces, can be a genreator
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

	def __rmatmul__(self, lhs: int) -> Dice:
		"""
			Rolls self LHS times and adds them together
		"""
		if neg := lhs < 0:
			lhs *= -1
		res = self
		for _ in range(lhs-1):
			res = res+self
		return -res if neg else res

	
	def _unary_level0(self, ops:callable) -> Dice:
		return Dice(self._rounding(ops(i)) for i in self)

	def __neg__(self) -> Dice:
		return self._unary_level0(op.neg)
	
	def __pos__(self) -> Dice:
		return self._unary_level0(op.pos)
	
	def __invert__(self) -> Dice:
		return self._unary_level0(op.invert)
	

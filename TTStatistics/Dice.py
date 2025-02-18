from typing import Generator
from itertools import product
import operator as op
from TTStatistics._parser import faces_to_prop
from TTStatistics.types import primitives
import TTStatistics.Pool as Pool 

type Dice = Dice
type Pool = Pool.Pool

class Dice(object):
	def __init__(self, faces, /, mask = None, rounding = None):
		self._f, self._p, self._c = faces_to_prop(faces)		
		self._derived_attr()
		self._mask = mask if mask else None

	def _derived_attr(self):
		self._mean = sum([p*f for p, f in zip(self.c, self.p)])
		self._cdf = self._cumulative()

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
	def cdf(self) -> list:
		return self._cdf

	def copy(self) -> Dice:
		copy = Dice(i for i in self)
		return copy
	
	def _number_binary(self, rhs: int | float, operations:callable):
		return Dice(operations(i, rhs) for i in self)
	
	def __iter__(self) -> Generator[int | float]: # might need ot be text also when mask
		for f, c in zip(self.f, self.c):
			for _ in range(c):
				yield f
				
	def __contains__(self, value: any) -> bool:
		return value in self._f
	
	def _binary_level0(self, rhs: int | float, ops: callable ) -> Dice | Pool:
		if type(rhs) in primitives:
			return Dice(ops(f, rhs) for f in self)
		elif isinstance(rhs, Dice):
			raise NotImplemented
		else:
			raise Exception("Unexpected type in dice level 0")

	def __add__(self, rhs: int | float | Dice | Pool) -> Dice | Pool:
		"""
		only does level 0, if higher up we reverse the call.
		"""
		return self._binary_level0(rhs, op.add)
	
	def __sub__(self, rhs: int | float | Dice | Pool) -> Dice | Pool:
		return self._binary_level0(rhs, op.sub)

	def __mul__(self, rhs: int | float | Dice | Pool) -> Dice | Pool:
		return self._binary_level0(rhs, op.mul)

	def __truediv__(self, rhs: int | float | Dice | Pool) -> Dice | Pool:
		return self._binary_level0(rhs, op.truediv)

	def _cumulative(self) -> list:
		res = []
		for p in self.p:
			if res:
				res.append(p + res[-1])
			else:
				res.append(p)
		return res
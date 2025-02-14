from typing import Generator
from itertools import product
from TTStatistics._parser import faces_to_prop
import TTStatistics.Pool as Pool 

type Dice = Dice
type Pool = Pool.Pool

class Dice(object):
	def __init__(self, faces, /, mask = None):
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
		copy = Dice([])
		copy._c = self.c
		copy._p = self.p # should be getters and setters, so it easily change stuff
		copy._f = self.f
		return copy
	
	def __iter__(self) -> Generator[int | float]: # might need ot be text also when mask
		for f, c in zip(self.f, self.c):
			for _ in range(c):
				yield f
				
	def __contains__(self, value: any) -> bool:
		return value in self._f

	def __add__(self, rhs) -> Dice | Pool:
		if isinstance(rhs, Dice):
			return Pool((self, rhs))
		elif isinstance(rhs, int):
			return Dice(i+rhs for i in self) # We could copy self and just add rhs to faces
		else:
			raise Exception("TODO add error dice")
		
	def _cumulative(self) -> list:
		res = []
		for p in self.p:
			if res:
				res.append(p + res[-1])
			else:
				res.append(p)
		return res
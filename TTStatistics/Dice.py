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

	@property
	def f(self) -> list:
		return self._f

	@property
	def p(self) -> list:
		return self._p
	
	def copy(self) -> Dice:
		res = Dice([])
		res._c = self._c
		res._p = self._p
		res._f = self._f
	
	def __iter__(self):
		for f, c in zip(self.f, self.c):
			for _ in range(c):
				yield f

	def __add__(self, rhs) -> Dice | Pool:
		if isinstance(rhs, Dice):
			return Pool((self, rhs))
		elif isinstance(rhs, int):
			return Dice(i+rhs for i in self) # We could copy self and just add rhs to faces
		else:
			raise Exception("TODO add error dice")
		
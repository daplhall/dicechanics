from itertools import product
from ._parser import parse_to_prop, int_to_prop

type Dice = Dice

class Dice(object):

	def __init__(self, inp, /, mask = None):
		if isinstance(inp, int):
			self._f, self._p, self._c = int_to_prop(1, inp)
		elif isinstance(inp, str):
			self._f, self._p, self._c = parse_to_prop(inp)
		else:
			raise Exception("Input not supported")
		if mask:
			self._mask = mask
	@property
	def f(self) -> list:
		return self._f

	@property
	def p(self) -> list:
		return self._p

	def __add__(self, rhs) -> Dice:
		raise NotImplemented()

class Zice(Dice):
	def __init__(self, inp, /, mask = None):
		super().__init__(inp, mask)
		if isinstance(inp, int):
			self._f, self._p, self._c = int_to_prop(0, inp)
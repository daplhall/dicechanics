from scipy.signal import fftconvolve

from ._textparser import parse_to_prop
from ._math import add_unique

def convolve(rhs, lhs):
	return fftconvolve(rhs,lhs).tolist()

class Dice(object):
	def __init__(self, inp, /, mask = None):
		if isinstance(inp, int):
			self._f = list(range(1, inp + 1))
			self._p = [1/len(self.f) for _ in self.f]
		elif isinstance(inp, str):
			self._f, self._p = parse_to_prop(inp)
		else:
			raise Exception("Input not supported")
		if mask:
			self._mask = mask
	@property
	def f(self):
		return self._f

	@property
	def p(self):
		return self._p

	def __add__(self, rh):
		res = Dice(0)	
		if isinstance(rh, (int,float)):
			res._f = [i + rh for i in self._f]
			res._p = self._p
		elif isinstance(rh, Dice): # NOTE this doesn't work when faces are not directly next to one another
			res._p = convolve(self._p, rh._p)
			res._f = add_unique(self._f, rh._f)
		else:
			raise Exception("Type is not supported in addtions")
		return res

class Zice(Dice):
	def __init__(self, inp, /, mask = None):
		Dice.__init__(self, inp, mask)
		if isinstance(inp, int):
			self._f = list(range(0, inp+1))
			self._p = [1/len(self.f) for _ in self.f]
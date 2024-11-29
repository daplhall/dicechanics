from scipy.signal import fftconvolve

from ._textparser import parse_to_prop

convolve = fftconvolve

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
		if isinstance(rh, (int,float)):
			self._f = [i + rh for i in self._f]
		elif isinstance(rh, Dice):
			pass	
		else:
			raise Exception("Type is not supported in addtions")

class Zice(Dice):
	def __init__(self, inp, /, mask = None):
		Dice.__init__(self, inp, mask)
		if isinstance(inp, int):
			self._f = list(range(0, inp+1))
			self._p = [1/len(self.f) for _ in self.f]
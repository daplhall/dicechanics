from itertools import product
from TTStatistics._parser import faces_to_prop
import TTStatistics as tts

type Dice = Dice
type Pool = tts.Pool

class Dice(object):

	def __init__(self, faces, /, mask = None):
		self._f, self._p, self._c = faces_to_prop(faces)		
		if mask:
			self._mask = mask
	@property
	def f(self) -> list:
		return self._f

	@property
	def p(self) -> list:
		return self._p

	def __add__(self, rhs) -> Dice | Pool:

		raise NotImplemented()
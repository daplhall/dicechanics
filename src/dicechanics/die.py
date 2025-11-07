from dicechanics.pool import Pool
from dicechanics.protocols.mapping import Mapping


class Die(Mapping):
	def __bool__(self):
		return False

	def __add__(self, rhs: "Die"):
		return Pool([self, rhs])

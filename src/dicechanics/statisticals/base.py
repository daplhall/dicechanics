from collections import defaultdict
from collections.abc import Callable

from dicechanics.protocols.statistical import Statistical


class BaseStatistical[T](Statistical):
	def __init__(self, data: dict[T, float] = {}):
		self.internalData = data

	def __bool__(self):
		return bool(self.internalData)

	def items(self):
		return self.internalData.items()

	def keys(self):
		return self.internalData.keys()

	def values(self):
		return self.internalData.values()

	def map(self, mapping: Callable[[T], T]):
		newInternalData = defaultdict(float)
		for key, value in self.items():
			newInternalData[mapping(key)] += value
		return type(self)(newInternalData)

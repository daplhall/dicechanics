from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable

from ttstatistics.dicechanics import protocols


class BaseStatistical[T](protocols.Statistical):
	def __init__(self, data: dict[T, float] = {}):
		self.probability = data

	def __bool__(self):
		return bool(self.probability)

	def items(self):
		return self.probability.items()

	def keys(self):
		return self.probability.keys()

	def values(self):
		return self.probability.values()

	def map(self, mapping: Callable[[T], T]) -> protocols.Statistical:
		newInternalData = defaultdict(float)
		for key, value in self.items():
			newInternalData[mapping(key)] += value
		return type(self)(newInternalData)

	def normalize(self) -> BaseStatistical:
		norm = sum(self.values())
		self.probability = {key: value / norm for key, value in self.items()}
		return self

	@property
	def mean(self):
		return None

	@property
	def varians(self):
		return None

	@property
	def std(self):
		return None

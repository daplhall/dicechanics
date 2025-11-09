import math
from numbers import Number

from ttstatistics.dicechanics.statisticals.base import BaseStatistical


class ScalarStatistical(BaseStatistical):
	def __init__(self, data: dict[Number, float] = {}):
		super().__init__(data)

	@property
	def mean(self):
		return sum(p * key for key, p in self.items())

	@property
	def varians(self):
		mean = self.mean
		return sum((key - mean) ** 2 for key in self.keys())

	@property
	def std(self):
		return math.sqrt(self.varians)

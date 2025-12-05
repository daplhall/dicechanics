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
		mu = self.mean
		return sum(p * (x - mu) ** 2 for x, p in self.items())

	@property
	def std(self):
		return math.sqrt(self.varians)

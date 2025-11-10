from collections.abc import Callable

from ttstatistics.core.protocols.base import (
	Unit,
)
from ttstatistics.dicechanics import protocols
from ttstatistics.dicechanics.protocols import Statistical
from ttstatistics.dicechanics.statisticals.scalar import ScalarStatistical


class Die(protocols.Die):
	def __init__(self, data: Statistical[Unit] = ScalarStatistical()):
		self.statisticalData: Statistical = data

	def __bool__(self):
		return False

	@property
	def mean(self):
		return self.statisticalData.mean

	@property
	def varians(self):
		return self.statisticalData.varians

	@property
	def std(self):
		return self.statisticalData.std

	def items(self):
		return self.statisticalData.items()

	def map(self, mapping: Callable[[Unit], Unit]) -> protocols.Die:
		return type(self)(self.statisticalData.map(mapping))

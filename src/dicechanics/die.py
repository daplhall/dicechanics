from collections.abc import Callable

from dicechanics import protocols
from dicechanics.protocols import Statistical
from dicechanics.protocols.base import (
	Unit,
)
from dicechanics.statisticals.scalar import ScalarStatistical


class Die(protocols.Die):
	def __init__(self, data: Statistical[Unit] = ScalarStatistical()):
		self.internalData: Statistical = data

	def __bool__(self):
		return False

	@property
	def mean(self):
		return self.internalData.mean

	@property
	def varians(self):
		return self.internalData.varians

	@property
	def std(self):
		return self.internalData.std

	def items(self):
		return self.internalData.items()

	def map(self, mapping: Callable[[Unit], Unit]) -> protocols.Die:
		return type(self)(self.internalData.map(mapping))

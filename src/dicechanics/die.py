from collections import defaultdict
from collections.abc import Callable

from dicechanics import operators
from dicechanics.pool import Pool
from dicechanics.protocols.base import AddUnit, MulUnit, Unit
from dicechanics.protocols.mapping import Mapping
from dicechanics.protocols.statistical import Statistical
from dicechanics.statisticals.scalar import ScalarStatistical


class Die(Mapping):
	def __init__(self, data: Statistical = ScalarStatistical()):
		self.internalData: Statistical = data

	def __bool__(self):
		return False

	def binary(
		self, rhs: Unit, operator: Callable[[Unit, Unit], Unit]
	) -> Mapping:
		newInternalData: dict = defaultdict(float)
		for key, val in self.internalData.items():
			newInternalData[operator(key, rhs)] += val
		statistical = type(self.internalData)(newInternalData)
		return Die(statistical)

	def __add__(self, rhs: Mapping | AddUnit) -> Mapping | Pool:
		if isinstance(rhs, Mapping):
			return Pool.from_list([self, rhs])
		elif isinstance(rhs, AddUnit):
			return self.binary(rhs, operators.add)
		else:
			raise ValueError("Unsupported Type")

	def __mul__(self, rhs: MulUnit) -> Mapping:
		return self.binary(rhs, operators.mul)

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

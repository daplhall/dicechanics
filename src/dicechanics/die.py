from collections.abc import Callable

from dicechanics import operators
from dicechanics.pool import Pool
from dicechanics.protocols.base import (
	AddUnit,
	DivUnit,
	MulUnit,
	SubUnit,
	Unit,
)
from dicechanics.protocols.mapping import Mapping
from dicechanics.protocols.statistical import Statistical
from dicechanics.statisticals.scalar import ScalarStatistical


class Die(Mapping):
	def __init__(self, data: Statistical[Unit] = ScalarStatistical()):
		self.internalData: Statistical = data

	def __bool__(self):
		return False

	def binaryOperation(
		self, rhs: Unit, operator: Callable[[Unit, Unit], Unit]
	) -> Mapping:
		return self.map(lambda x: operator(x, rhs))

	def __add__(self, rhs: Mapping | AddUnit) -> Mapping | Pool:
		if isinstance(rhs, Mapping):
			return Pool.from_list([self, rhs])
		elif isinstance(rhs, AddUnit):
			return self.binaryOperation(rhs, operators.add)
		else:
			raise ValueError("Unsupported Type")

	def __mul__(self, rhs: MulUnit) -> Mapping:
		return self.binaryOperation(rhs, operators.mul)

	def __sub__(self, rhs: SubUnit) -> Mapping:
		return self.binaryOperation(rhs, operators.sub)

	def __truediv__(self, rhs: DivUnit) -> Mapping:
		return self.binaryOperation(rhs, operators.div)

	def __floordiv__(self, rhs: DivUnit) -> Mapping:
		return self.binaryOperation(rhs, operators.floorDiv)

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

	def map(self, mapping: Callable[[Unit], Unit]) -> Mapping:
		return type(self)(self.internalData.map(mapping))

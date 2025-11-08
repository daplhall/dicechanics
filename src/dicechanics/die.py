from collections.abc import Callable

from dicechanics import operators, protocols
from dicechanics.pool import Pool
from dicechanics.protocols import Mapping, Statistical
from dicechanics.protocols.base import (
	AddUnit,
	DivUnit,
	MulUnit,
	SubUnit,
	Unit,
)
from dicechanics.statisticals.scalar import ScalarStatistical


class Die(protocols.Die):
	def __init__(self, data: Statistical[Unit] = ScalarStatistical()):
		self.internalData: Statistical = data

	def __bool__(self):
		return False

	def binaryOperation(
		self, rhs: Unit, operator: Callable[[Unit, Unit], Unit]
	) -> protocols.Die:
		return self.map(lambda x: operator(x, rhs))

	def __add__(self, rhs: protocols.Die | AddUnit) -> protocols.Die | Pool:
		if isinstance(rhs, protocols.Die):
			return Pool.from_list([self, rhs])
		elif isinstance(rhs, AddUnit):
			return self.binaryOperation(rhs, operators.add)
		else:
			raise ValueError("Unsupported Type")

	def __mul__(self, rhs: MulUnit) -> protocols.Die:
		return self.binaryOperation(rhs, operators.mul)

	def __sub__(self, rhs: SubUnit) -> protocols.Die:
		return self.binaryOperation(rhs, operators.sub)

	def __truediv__(self, rhs: DivUnit) -> protocols.Die:
		return self.binaryOperation(rhs, operators.div)

	def __floordiv__(self, rhs: DivUnit) -> protocols.Die:
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

	def map(self, mapping: Callable[[Unit], Unit]) -> protocols.Die:
		return type(self)(self.internalData.map(mapping))

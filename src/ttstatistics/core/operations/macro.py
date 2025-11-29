from ttstatistics.core import protocols
from ttstatistics.core.operations.combinations import (
	RegularCombination,
	Selective,
)


def basePerformOnGroup(
	bag: protocols.Group, operation, combineor
) -> protocols.Mapping:
	combineMachine = combineor()
	return combineMachine.calculate(bag, operation)


def selectiveOnGroup(bag: protocols.Group, operation) -> protocols.Mapping:
	return basePerformOnGroup(bag, operation, Selective)


def regularOnGroup(bag: protocols.Group, operation) -> protocols.Mapping:
	return basePerformOnGroup(bag, operation, RegularCombination)

from ttstatistics.core import protocols
from ttstatistics.core.genericmapping import GenericMapping
from ttstatistics.core.operations.combinations import (
	RegularCombination,
	Selective,
	getOutcomes,
)
from ttstatistics.utils.reference import Reference


def normalize(statisticalDict):
	norm = sum(statisticalDict.values())
	return {
		key: round(value / norm, 15) for key, value in statisticalDict.items()
	}


class Operators:
	@staticmethod
	def performOnBag(bag: protocols.Group, operation):
		if bagSlice := bag.prepareSlice():
			outcomes, meta = getOutcomes(bag)
			comb = Selective()
			slice_ = tuple(bagSlice.next() for _ in range(sum(meta)))
			res = comb.calculate(outcomes, operation, sum(meta), meta, slice_)
		else:
			comb = RegularCombination()
			res = comb.calculate(
				list(bag.prepare()), operation, 0, Reference(None)
			)
		return GenericMapping(normalize(res))

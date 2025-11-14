from ttstatistics.core import protocols
from ttstatistics.core.genericmapping import GenericMapping
from ttstatistics.core.operations.combinatorics import (
	combinations,
	getOutcomes,
	selective,
)
from ttstatistics.utils.reference import Reference


def normalize(statisticalDict):
	norm = sum(statisticalDict.values())
	return {
		key: round(value / norm, 15) for key, value in statisticalDict.items()
	}


class Operators:
	@staticmethod
	def performOnBag(bag: protocols.Bag, operation):
		if bagSlice := bag.prepareSlice():
			outcomes, meta = getOutcomes(bag)
			res = selective(outcomes, operation, sum(meta), meta, bagSlice)
		else:
			res = combinations(
				list(bag.prepare()), operation, 0, Reference(None)
			)
		return GenericMapping(normalize(res))

from collections import defaultdict
from collections.abc import Callable

from dicechanics.protocols.base import Unit
from dicechanics.utils.reference import Reference

type BagItems = list[tuple[Unit, int]]


class Combinatorics:
	@staticmethod
	def combinations(
		items: BagItems,
		operation: Callable[[Unit, Unit], Unit],
		layer: int,
		mem: Reference,
	):
		if mem:
			return mem.get()
		if Combinatorics.isEndOfItems(items, layer):
			return {}
		res = defaultdict(int)
		mapping, count = Combinatorics.countDownAmount(items, layer)
		for key, value in mapping.items():
			if sub := Combinatorics.combinations(
				items,
				operation,
				Combinatorics.whichLayerNext(layer, count),
				mem,
			):
				for skey, svalue in sub.items():
					res[operation(key, skey)] += svalue * value
			else:
				res[key] = value
		mem.set(res)
		return res

	@staticmethod
	def countDownAmount(items: BagItems, layer: int):
		mapping, count = items[layer]
		items[layer] = mapping, count - 1
		return mapping, count

	@staticmethod
	def whichLayerNext(layer: int, count: int):
		return layer + 1 if count <= 1 else layer

	@staticmethod
	def isEndOfItems(items: BagItems, layer: int):
		return layer >= len(items)

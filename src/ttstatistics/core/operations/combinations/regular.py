from collections import defaultdict
from collections.abc import Callable

from ttstatistics.core.protocols.base import Unit
from ttstatistics.utils.reference import Reference

type BagItems = list[tuple[Unit, int]]


def updateWithOperations(current, subproblem, operation, res):
	key, value = current
	for skey, svalue in subproblem.items():
		res[operation(key, skey)] += svalue * value


def updateNoSubproblem(current, res):
	key, value = current
	res[key] = value


def countDownAmount(items: BagItems, layer: int):
	mapping, count = items[layer]
	items[layer] = mapping, count - 1
	return mapping, count


def whoIsNext(layer: int, count: int):
	return layer + 1 if count <= 1 else layer


def isEndOfBranch(items: BagItems, layer: int):
	return layer >= len(items)


class RegularCombination:
	def calculate(
		self,
		items: BagItems,
		operation: Callable[[Unit, Unit], Unit],
		whom: int,
		mem: Reference,
	):
		if mem:
			return mem.get()
		if isEndOfBranch(items, whom):
			return {}
		res = defaultdict(int)
		mapping, count = countDownAmount(items, whom)
		for curr in mapping.items():
			if sub := self.calculate(
				items,
				operation,
				whoIsNext(whom, count),
				mem,
			):
				updateWithOperations(curr, sub, operation, res)
			else:
				updateNoSubproblem(curr, res)
		mem.set(res)
		return res

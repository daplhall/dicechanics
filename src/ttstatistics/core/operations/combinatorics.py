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


def combinations(
	items: BagItems,
	operation: Callable[[Unit, Unit], Unit],
	layer: int,
	mem: Reference,
):
	if mem:
		return mem.get()
	if isEndOfBranch(items, layer):
		return {}
	res = defaultdict(int)
	mapping, count = countDownAmount(items, layer)
	for curr in mapping.items():
		if sub := combinations(
			items,
			operation,
			whoIsNext(layer, count),
			mem,
		):
			updateWithOperations(curr, sub, operation, res)
		else:
			updateNoSubproblem(curr, res)
	mem.set(res)
	return res

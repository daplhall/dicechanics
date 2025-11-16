__all__ = ["RegularCombination"]
from collections import defaultdict

from ttstatistics.core import protocols
from ttstatistics.utils.reference import Reference


def updateWithOperations(current, subproblem, operation, res):
	key, value = current
	for skey, svalue in subproblem.items():
		res[operation(key, skey)] += svalue * value


def updateNoSubproblem(current, res):
	key, value = current
	res[key] = value


def countDownAmount(items: protocols.GroupItems, layer: int):
	mapping, count = items[layer]
	items[layer] = mapping, count - 1
	return mapping, count


def whoIsNext(layer: int, count: int):
	return layer + 1 if count <= 1 else layer


def isEndOfBranch(items: protocols.GroupItems, layer: int):
	return layer >= len(items)


class RegularCombination:
	def calculate(
		self, group: protocols.Group, operation: protocols.InputFunction
	):
		return self._evaluate(
			list(group.prepare()), operation, 0, Reference(None)
		)

	def _evaluate(
		self,
		items: protocols.GroupItems,
		operation: protocols.InputFunction,
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
			if sub := self._evaluate(
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

__all__ = ["RegularCombination"]
from collections import defaultdict
from functools import cache

from ttstatistics.core import protocols
from ttstatistics.core.empty import VariableCount
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


class RegularCombinationBenchmark:
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
		if not isinstance(count, VariableCount):
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
		else:
			for n in count.counts.items():
				count.max_
				pass
		mem.set(res)
		return res


class RegularCombination:
	def calculate(
		self, group: protocols.Group, operation: protocols.InputFunction
	):
		return self._evaluate(tuple(group.prepare()), operation)

	@cache
	def _evaluate(
		self,
		items: protocols.GroupItems,
		operation: protocols.InputFunction,
	):
		if not items:
			return {}
		mapping, amount = items[0]
		if not isinstance(amount, VariableCount):
			curr = self._accumulate(mapping, amount, operation)
			if sub := self._evaluate(items[1:], operation):
				res = self._combine(curr, sub, operation)
			else:
				res = curr
		else:
			res = defaultdict(int)
			for n, w in amount.counts.items():
				curr = self._accumulate(mapping, n, operation)
				if sub := self._evaluate(items[1:], operation):
					tmp = self._combine(curr, sub, operation)
				else:
					tmp = curr
				for key, weight in tmp.items():
					res[key] += weight * w
		return res

	@cache
	def _accumulate(self, mapping, amount, operation):
		if amount == 0:
			return None
		res = defaultdict(int)
		for curr in mapping.items():
			sub = self._accumulate(mapping, amount - 1, operation)
			if sub is not None:
				updateWithOperations(curr, sub, operation, res)
			else:
				updateNoSubproblem(curr, res)
		return res

	def _combine(self, curr, sub, operation):
		res = defaultdict(int)
		for curr in curr.items():
			updateWithOperations(curr, sub, operation, res)
		return res

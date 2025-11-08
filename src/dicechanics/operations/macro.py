from collections import defaultdict
from typing import Any


class Reference:
	"""
	A Reference class, which acts like a pointer.
	None is use as NULL
	"""

	def __init__(self, referenced_item: Any):
		self._ref = referenced_item

	def get(self) -> Any:
		"""
		Returns the value references by the "pointer".

		Returns
		-------
		out: Any
			The object pointed to.
		"""
		return self._ref

	def set(self, new_ref: Any):
		"""
		Sets the value in the pointer
		"""
		self._ref = new_ref

	def __bool__(self):
		"""
		Evaluates if something is stored in the reference.
		"""
		return self._ref is not None


def countDownAmount(items, layer):
	mapping, count = items[layer]
	items[layer] = mapping, count - 1
	return mapping, count


def whichLayerNext(layer, count):
	return layer + 1 if count <= 1 else layer


def isEndOfItems(items, layer):
	return layer >= len(items)


class Combinatorics:
	@staticmethod
	def combinations(items, operation, layer, mem):
		if mem:
			return mem.get()
		if isEndOfItems(items, layer):
			return {}
		res = defaultdict(lambda: 0)
		mapping, count = countDownAmount(items, layer)
		for key, value in mapping.items():
			if sub := Combinatorics.combinations(
				items, operation, whichLayerNext(layer, count), mem
			):
				for skey, svalue in sub.items():
					res[operation(key, skey)] += svalue * value
			else:
				res[key] = value
		mem.set(res)
		return res


"""
if mem:
	return mem.get()
if layer >= len(inpt):
	return {}
res: T = defaultdict(int)
for f, c in inpt[layer].items():
	if sub := linear_combs(inpt, layer + 1, func, mem):
		for sf, sc in sub.items():
			res[func(f, sf)] += c * sc
	else:
		res[f] = c
mem.set(res)
return res
"""


def perform(bag, operation):
	res = Combinatorics.combinations(
		list(bag.items()), operation, 0, Reference(None)
	)
	norm = sum(res.values())
	q = {key: round(value / norm, 15) for key, value in res.items()}
	return type(bag)(q)


"""
	res = defaultdict(lambda: 1)
	for mapping, count in bag.items():
		for key, value in mapping.items():
			res[key] *= value * count
	norm = sum(res.values())
	return type(bag)({key: value / norm for key, value in res.items()})
"""

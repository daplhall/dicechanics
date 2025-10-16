from collections import defaultdict
from typing import Sequence

import dicechanics as ds
from dicechanics._popper import DicePopper
from dicechanics._referance import Reference
from dicechanics._typing import BinaryFunc_T

type T = dict[object, int]
type Inpt_T = Sequence[ds.Die]
type Bag_T = Sequence[DicePopper]
type Mem_T = dict[object, T]

ARRAY_START_INDEX = 0


def linear_combs(
	inpt: Inpt_T, layer: int, func: BinaryFunc_T, mem: Reference
) -> T:
	"""
	Function that applies a linear operation to a set of unordered combinations

	Parameters
	----------
	inpt: Sequence
		A sequence of Die.
	layer: int
		An integer that should always be 0 when first called.
	func: Callable
		The function that is applied to the set of outcomes.
		Takes values at a time and combines them.
	mem: dict
		The cache in which each layer is saved

	Returns
	-------
	out : dict
		A dict with the outcomes as keys and occurrences as data


	Developer notes
	---------------
	We use mem as a pointer, such that each layer can modify and access it,
	hence the `0` indexing in mem
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


def linear_non_selective(inpt: Inpt_T, func: BinaryFunc_T) -> ds.Die:
	"""
	The function that sets up the parameters for linear_combs

	Parameters
	----------
	inpt: Sequence
		A sequence of dice.
	func: Callable
		The function that is applied to the set of outcomes.
		Takes values at a time and combines them.

	Returns
	-------
		the result of the combinatorics calculations in the form of
		a die representation.
	"""

	res = linear_combs(inpt, ARRAY_START_INDEX, func, Reference(None))
	return ds.Die(res)


def selective_comb(
	bag: Bag_T, func: BinaryFunc_T, keep: list[int], mem: Mem_T
) -> T:
	"""
	Function that goes through the combinatorics of ordered outcomes.

	Parameters
	----------
	bag: Sequence
		A sequence of DicePoppers.
	func: Callable
		The function that is applied to the set of outcomes.
		Takes values at a time and combines them.
	keep: list
		List of which dice in bag to keep.
	mem: dict
		The cache in which each layer is saved
	"""
	cache_key = tuple(i.identifier() for i in bag)
	if cache_key in mem:
		return mem[cache_key]
	if not bag:
		mem[cache_key] = {None: 1}
		return mem[cache_key]
	res: T = defaultdict(int)
	sorted_bag = sorted(bag, key=lambda key: key.max(), reverse=True)
	while dice := sorted_bag[0]:
		o, c = dice.pop()
		sub_bag = [i.copy() for i in sorted_bag[1:]]
		sub = selective_comb(sub_bag, func, keep[:-1], mem)
		for sf, sc in sub.items():
			if keep[-1] == 0:
				key = sf if sf is not None else None
			elif sf is None:
				key = o
			else:
				key = func(o, sf)
			res[key] += c * sc
		if sorted_bag[0]:
			sorted_bag.sort(key=lambda key: key.max(), reverse=True)
	mem[cache_key] = res
	return res


def linear_selective(
	inpt: Inpt_T, keep: list[int], func: BinaryFunc_T
) -> ds.Die:
	"""
	Function that applies a linear operation to a set of ordered combinations

	Parameters
	----------
	inpt: Sequence
		A sequence of dice.
	keep: list
		List of which dice in bag to keep.
	func: Callable
		The function that is applied to the set of outcomes.
		Takes values at a time and combines them.

	Returns
	-------
		the result of the combinatorics calculations in the form of
		a die representation.
	"""
	mem: Mem_T = {}
	poppers = [DicePopper(i) for i in inpt]
	res = selective_comb(poppers, func, keep, mem)
	return ds.Die(res)

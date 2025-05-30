from collections import defaultdict
import DiceStatistics as ds
from DiceStatistics._popper import DicePopper


def linear_combs(inpt: list[ds.Dice], layer:int , func: callable, mem: dict) -> defaultdict[int]:
	if layer in mem:
		return mem[layer]
	if layer >= len(inpt):
		return {}
	res = defaultdict(int)
	for f,c in inpt[layer].items():
		if sub := linear_combs(inpt, layer+1, func, mem):
			for sf,sc in sub.items():
				res[func(f,sf)] += c*sc
		else:
			res[f] = c
	mem[layer] = res
	return res

def linear_non_selective(inpt: list[ds.Dice], func: callable) -> ds.Dice:
	mem = {}
	res = linear_combs(inpt, 0, func, mem)
	return ds.Dice.from_dict(res)

def selective_comb(bag, func, keep, mem):
	"""
	TODO:
	The popper goes through them 1 by 1 so if we have a face with repeated 1000 times it runs through that 1000 times...	
	"""
	cache_key = tuple(i.identifier() for i in bag)	
	if cache_key in mem:
		return mem[cache_key]
	if not bag:
		mem[cache_key] = {None: 1}
		return mem[cache_key]
	res = defaultdict(int)
	sorted_bag = sorted(bag, key = lambda key: key.max(), reverse=True)
	while(dice := sorted_bag[0]):
		o,c = dice.pop() 
		sub_bag = [i.copy() for i in sorted_bag[1:]]
		sub = selective_comb(sub_bag, func, keep[:-1], mem) 
		for sf, sc in sub.items():
			if keep[-1] == 0:
				key = sf if sf is not None else None
			elif sf is None:
				key = o
			else:
				key= func(o,sf)
			res[key] += c*sc
		if sorted_bag and len(sorted_bag) > 1 and sorted_bag[0]:
			sorted_bag.sort(key = lambda key: key.max(), reverse=True)
	mem[cache_key] = res
	return res

def linear_selective(inpt: list[ds.Dice], keep: list[int], func: callable) -> ds.Dice:
	mem = {}
	inpt = [DicePopper(i) for i in inpt]
	res = selective_comb(inpt, func, keep, mem)
	return ds.Dice.from_dict(res)

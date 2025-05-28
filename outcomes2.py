from line_profiler import profile
from itertools import compress
from collections import ChainMap, defaultdict
from math import prod, factorial
from copy import deepcopy

from DiceStatistics import d, Dice
from DiceStatistics._popper import DicePopper

def _max(key):
	if not key:
		return None
	return max(key)
		
def comb(bag, func, keep, mem):
	cache_key = tuple(i.identifier() for i in bag)	
	if cache_key in mem:
		return mem[cache_key]
	if not bag:
		mem[cache_key] = {None: 1}
		return mem[cache_key]
	res = defaultdict(int)
	sorted_bag = sorted(bag, key = lambda key: key.max(), reverse=True)
	while(dice := sorted_bag[0]):
		o = dice.pop() 
		sub_bag = [i.copy() for i in sorted_bag[1:]]
		sub = comb(sub_bag, func, keep[:-1], mem) 
		for sf, sc in sub.items():
			if keep[-1] == 0:
				key = sf if sf is not None else None
			elif sf is None:
				key = o
			else:
				key= func(o,sf)
			res[key] += sc
		if sorted_bag and len(sorted_bag) > 1 and sorted_bag[0]:
			sorted_bag = sorted(sorted_bag, key = lambda key: key.max(), reverse=True)
	mem[cache_key] = res
	return res

def selective_combs(bag, keep, func):
	mem = {}
	pop_bag = [DicePopper(i) for i in bag]
	res = comb(pop_bag, func, keep, mem)
	return res


bag = [
		Dice.from_dict({1:1,2:1,3:1,4:1}),
		Dice.from_dict({2:1,3:1,4:1,5:1}),
		Dice.from_dict({3:1,4:1,5:1,6:1}),
		Dice.from_dict({4:1,5:1,6:1,7:1})
]

bag = [
	d(6),
]*3


keep = [0,1,1]

import time
t = time.time()
res = selective_combs(bag, keep, lambda x, y: x+y)
d = Dice.from_dict(res)
print(d)
#q = bag[0] + bag[1] + bag[2] + bag[3]
#print(d._data == q._data)
print(time.time() - t)
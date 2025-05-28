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
		
CALLS = 0
HITS = 0
LOOPS = 0
@profile
def comb(bag, func, keep, mem):
	global HITS, CALLS, LOOPS
	CALLS += 1
	cache_key = tuple(i.identifier() for i in bag)	
	if cache_key in mem:
		HITS += 1
		return mem[cache_key]
	if not bag:
		mem[cache_key] = {None: 1}
		return mem[cache_key]
	res = defaultdict(int)
	sorted_bag = sorted(bag, key = lambda key: key.max(), reverse=True)
	while(dice := sorted_bag[0]):
		LOOPS += 1
		o = dice.pop() 
		sub_bag = [i.copy() for i in sorted_bag[1:]]
		sub = comb(sub_bag, func, keep[:-1], mem) 
		for sf, sc in sub.items():
			if keep[-1] == 0 and sf is not None:
				key = sf
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

#bag = [
#	d(50),
#]*5


keep = [1]*len(bag)

import time
t = time.time()
res = selective_combs(bag, keep, lambda x, y: x+y)
d = Dice.from_dict(res)
print(time.time() - t)
print("CALLS:", CALLS)
print("HITS:", HITS)
print("LOOPS:", LOOPS)
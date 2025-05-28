from line_profiler import profile
from itertools import compress
from collections import ChainMap, defaultdict
from math import prod, factorial
from copy import deepcopy

from DiceStatistics import d, Dice

def _max(key):
	if not key:
		return None
	return max(key)
		
HITS = 0
CALLS = 0
LOOPS = 0
"""
This function might be faster than the rest
"""
@profile
def comb(bag, idxs, func, keep, mem, I):
	global CALLS, HITS, LOOPS
	CALLS += 1
	cache_key = tuple(tuple(i) for i in bag)
	if cache_key in mem:
		HITS+=1
		#print("\thit:", bag)
		return mem[cache_key]

	if not bag:
		res = {None: 1}
		mem[cache_key] = res
		return res

	res = defaultdict(int)
	sorted_bag, sorted_idxs = zip(*sorted(zip(bag,idxs), key = lambda key: _max(key[0]), reverse=True))
	sorted_bag = list(sorted_bag)
	while(sorted_bag[0]):
		LOOPS += 1
		o = sorted_bag[0][-1] if keep[-1] else None
		c = 1
		sorted_bag[0] = sorted_bag[0][:-1]# "cheeper pop the top"
		sub_bag = sorted_bag[1:]
		sub_idxs = sorted_idxs[1:]
		sub = comb(sub_bag, sub_idxs, func, keep[:-1], mem, I+1)
		for sf, sc in sub.items():
			if o is None and sf is not None:
				key = sf
			elif sf is None:
				key = o
			else:
				key= func(o,sf)
			res[key] += c*sc
		if sorted_bag and len(sorted_bag) > 1 and sorted_bag[0]:
			sorted_bag, sorted_idxs = zip(*sorted(zip(sorted_bag,sorted_idxs), key = lambda key: _max(key[0]), reverse=True))
			sorted_bag = list(sorted_bag)
	mem[cache_key] = res
	return res

def f(x,y):
	if isinstance(y, int):
		return (x,y)
	return (x,) + y

bag = [
		[1,2,3,4],
		[2,3,4,5],
		[3,4,5,6],
		[4,5,6,7],
]

ER = 51
bag = [
	list(range(1,ER)),
]*5

keep = [1]*len(bag)
import time
mem = {}
t = time.time()
#res = comb(bag, list(range(len(bag))), lambda x,y: x+y, keep, mem)
res = comb(bag, list(range(len(bag))), lambda x,y: x+y, keep, mem,0)
print(time.time() - t)
q = Dice.from_dict(res)
print(q._units)
print("CALLS:", CALLS)
print("HITS:", HITS)
print("LOOPS:", LOOPS)
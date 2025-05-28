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
RE = 0
RE1 = 0
RE2 = 0
RE3 = 0
RE4 = 0
CACHEKEY = defaultdict(int)
"""
This function might be faster than the rest
"""
#:@profile
def comb(bag, idxs, func, keep, mem, I):
	global RE,HITS, RE1, RE2, RE3, RE4
	cache_key = tuple(tuple(i) for i in bag)
	if cache_key in mem:
		HITS+=1
		#print("\thit:", bag)
		#return mem[cache_key]

	if not bag:
		res = {None: 1}
		mem[cache_key] = res
		return res

	res = defaultdict(int)
	sorted_bag, sorted_idxs = zip(*sorted(zip(bag,idxs), key = lambda key: _max(key[0]), reverse=True))
	sorted_bag = list(sorted_bag)
	while(sorted_bag[0]):
		o = sorted_bag[0][-1] if keep[-1] else None
		c = 1
		sorted_bag[0] = sorted_bag[0][:-1]# "cheeper pop the top"
		sub_bag = sorted_bag[1:]
		sub_idxs = sorted_idxs[1:]
		if len(bag) == 4:
			RE+=1
			#print(o,sorted_idxs[0], sorted_bag[0],"\t", sub_bag, sub_idxs)
		if len(bag) == 3:
			RE1+=1
		if len(bag) == 2:
			RE2+=1
		if len(bag) == 1:
			RE3+=1
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
]*4

keep = [1]*len(bag)
import time
mem = {}
t = time.time()
#res = comb(bag, list(range(len(bag))), lambda x,y: x+y, keep, mem)
res = comb(bag, list(range(len(bag))), lambda x,y: x+y, keep, mem,0)
print(time.time() - t)
q = Dice.from_dict(res)
print(q._units)
#w = d(bag[0]) + d(bag[1]) + d(bag[2])+ d(bag[3])
#print(w)
print(HITS)
print("RE:")
print(RE)
print(RE1)
print(RE2)
print(RE3)
print(RE4)
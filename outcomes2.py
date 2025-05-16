from line_profiler import profile
from itertools import compress
from collections import ChainMap, defaultdict
from math import prod, factorial
from copy import deepcopy

from DiceStatistics import d, Dice

def _max(key):
	if not key:
		return None
	return min(key)
		
HITS = 0
CALLS = 0
RE = 0
CACHEKEY = defaultdict(int)
"""
the keep idea works we, we just need to know how to structure the order of the code corretly!
and then we need to find out if we can cache
"""
#:@profile
def comb(bag, idxs, func, keep, mem):
	global HITS, CALLS, RE
	CALLS+=1

	cache_key = tuple(tuple(i) for i in bag)
	#print(bag, idxs)
	if cache_key in mem:
		HITS +=1
		#print("\thit",bag, idxs,"\t\t",cache_key)
		#CACHEKEY[cache_key] += 1
		return mem[cache_key]
		
		
	if not bag:
		res = {None: 1}
		mem[cache_key] = res
		return res

	res = defaultdict(int)
	sorted_bag, sorted_idxs = zip(*sorted(zip(bag,idxs), key = lambda key: _max(key[0]), reverse=True))
	sorted_bag = list(sorted_bag)
	while(sorted_bag[0]):
		RE += 1
		o = sorted_bag[0][-1] if keep[-1] else None
		c = 1
		sorted_bag[0] = sorted_bag[0][:-1]# "cheeper pop the top"
		sub_bag = sorted_bag[1:]
		sub_idxs = sorted_idxs[1:]
		#if len(bag) == 4:
		print(o,sorted_idxs[0], sorted_bag[0], "\t", sub_bag, sub_idxs)
		ck = tuple(tuple(i) for i in sub_bag)
		if ck in mem:
			sub = mem[ck]
		else:
			sub = comb(sub_bag, sub_idxs, func, keep[:-1], mem)
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
		[4,5,6,7]
]

ER = 10
#bag = [
#	list(range(1,ER)),
#	list(range(1,ER)),
#	list(range(1,ER)),
#]
bag = [
	list(range(1,7)),
	list(range(1,5)),
]

keep = [0,1]
import time
mem = {}
t = time.time()
#res = comb(bag, list(range(len(bag))), lambda x,y: x+y, keep, mem)
res = comb(bag, list(range(len(bag))), lambda x,y: x+y, keep, mem)
print(time.time() - t)
q = Dice.from_dict(res)
print(q._units)
w = d(bag[0]) + d(bag[1])
print(q)
print(w)
print(HITS)
print(CALLS)
print(HITS/CALLS)
print(RE)
for f, c in CACHEKEY.items():
	print(f,c)

#from line_profiler import profile
from itertools import compress
from collections import ChainMap, defaultdict
from math import prod, factorial
from copy import deepcopy

from DiceStatistics import d, Dice

def _max(key):
	if not key:
		return None
	return max(key)

#@profile
HITS = 0
CALLS = 0
"""
the keep idea works we, we just need to know how to structure the order of the code corretly!
and then we need to find out if we can cache
"""
def dp(bag, idxs, func, keep, mem):
	global HITS, CALLS
	CALLS+=1
	cache_key = idxs
	if cache_key in mem:
		HITS += 1
		return mem[cache_key]
	res = defaultdict(int)
	C = 1 ## where this is used, we need to translate into dict
	if len(bag) == 1:
		for sf in bag[0]:
			res[(sf,sf)] = C
		#mem[cache_key] = res
		return res

	#sorted_bag = sorted(bag, key = lambda key: _max(key), reverse=True) # might need copy
	sorted_bag, sorted_idxs = zip(*sorted(zip(bag,idxs), key = lambda key: _max(key[0]), reverse=True))
	sorted_bag = list(sorted_bag)
	while(sorted_bag[0]):
		o = sorted_bag[0][-1]
		c = C
		sorted_bag[0] = sorted_bag[0][:-1]
		sub_bag = sorted_bag[1:]
		sub_idxs = sorted_idxs[1:]
		sub = dp(sub_bag, sub_idxs , func, keep, mem)
		for idx,((sf, p), sc) in enumerate(sub.items()):
			if p <= o:
				res[func(o,sf), o] += c*sc
		if sorted_bag and len(sorted_bag) > 1 and sorted_bag[0]: # i stop the code here if the current top is empty
			sorted_bag, sorted_idxs = zip(*sorted(zip(sorted_bag,idxs), key = lambda key: _max(key[0]), reverse=True))
			sorted_bag = list(sorted_bag)
	#mem[cache_key] = res
	return res
		

def f(x,y):
	if isinstance(y, int):
		return (x,y)
	return (x,) + y

bag = [
		list(range(1,7)),
		list(range(1,7)),
		list(range(1,7)),
]



keep = [0,1]

mem = {}
import time
t = time.time()
res = dp(bag, tuple(range(len(bag))), lambda x,y: x+y, keep, mem)
final = defaultdict(int)
for (f,_), c in res.items():
	final[f] += c
print(time.time()-t)
print(res)
print(final)
die = Dice.from_dict(final)
print(die)
print(4@d(6))
print(die.p)
print(HITS)
print(CALLS)
#res = comb(bag, f)

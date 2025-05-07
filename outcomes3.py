
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
def dp(bag, func, keep, mem):
	res = defaultdict(int)
	C = 1 ## where this is used, we need to translate into dict
	if len(bag) == 1:
		for sf in bag[0]:
			res[(sf,sf)] = C
		return res

	sorted_bag = sorted(bag, key = lambda key: _max(key), reverse=True) # might need copy
	while(sorted_bag[0]):
		o = sorted_bag[0][-1]
		c = C
		sorted_bag[0] = sorted_bag[0][:-1]
		sub_bag = sorted_bag[1:]
		sub = dp(sub_bag, func, keep, mem)
		for (sf, p), sc in sub.items():
			if p <= o:
				res[func(o,sf), o] += c*sc
		if sorted_bag and len(sorted_bag) > 1 and sorted_bag[0]:
			sorted_bag.sort(key = lambda key: _max(key), reverse=True)
	return res
		

def f(x,y):
	if isinstance(y, int):
		return (x,y)
	return (x,) + y

bag = [
	[1,2],
	[1,2],
	[1,2],
	[1,3],
]

keep = [0,1]

mem = {}
res = dp(bag, lambda x,y: x+y, keep, mem)
final = defaultdict(int)
for (f,_), c in res.items():
	final[f] += c
print(res)
print(final)
print(Dice.from_dict(final).p)
#res = comb(bag, f)

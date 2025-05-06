#from line_profiler import profile
from itertools import compress
from collections import ChainMap, defaultdict
from math import prod, factorial
from copy import deepcopy

from DiceStatistics import d, Dice

class outcomes(object):
	def __init__(self, outcomes, total):
		self._outcomes = outcomes
		self._max = max(outcomes) if outcomes else None
		self._total = total

	@classmethod
	def unique_outcomes(cls, bag:list):
		res = defaultdict(int)
		total = 0
		for die in bag:
			for f,c in die.items():
				res[f] += c
				total += c
		self = cls.__new__(cls)
		self.__init__(res, total)
		return self
	@classmethod
	def from_outcomes(cls, other):
		self = cls.__new__(cls)
		self._outcomes = other._outcomes.copy()
		self._max = other._max
		self._total = other._total
		return self
	
	def pop(self):
		outcomes = self._outcomes
		new = False
		if outcomes[self._max] == 0:
			outcomes.pop(self._max)
			self._max = max(outcomes)
			new = True
		outcomes[self._max] -= 1
		self._total -= 1
		return self._max, new
	
	def max(self):
		return self._max
	
	def copy(self):
		return outcomes.from_outcomes(self)
	
	def __str__(self):
		return "outcome(" + str(self._outcomes) + ')'
	
	def __repr__(self):
		return self.__str__()
	
	def __iter__(self):
		q = self.copy()
		for i in range(self._total):
			res = q.pop()
			yield res

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
def comb(bag, func, keep, mem):
	cache_key = (tuple(i) for i in bag)
	if cache_key in mem:
		return mem[cache_key]
		
	if not bag:
		return {None:1}

	sorted_bag = sorted(bag, key = lambda key: _max(key), reverse=True) # might need copy
	res = defaultdict(int)
	while(sorted_bag[0]):
		o = sorted_bag[0][-1] if keep[-1] else None
		sorted_bag[0] = sorted_bag[0][:-1]# "pop the top"
		c = 1
		sub_bag = sorted_bag[1:]
		sub = comb(sub_bag, func, keep[:-1], mem)
		for sf, sc in sub.items():
			if o is None and sf is not None:
				key = sf
			elif sf is None:
				key = o
			else:
				key= func(o,sf)
			res[key] += c*sc
		if sorted_bag and len(sorted_bag) > 1 and sorted_bag[0]:
			sorted_bag.sort(key = lambda key: _max(key), reverse=True)
	mem[cache_key] = res
	return res

def f(x,y):
	if isinstance(y, int):
		return (x,y)
	return (x,) + y

bag = [
	[1,2],
	[1,2],
	[1,2],
	[1,2]
]

keep = [0,1,0,1]

mem = {}
res = comb(bag, lambda x,y: x+y, keep, mem)
#res = comb(bag, f)
q = Dice.from_dict(res)
print(q)
print(q.p)

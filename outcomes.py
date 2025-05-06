#from line_profiler import profile
from itertools import compress
from collections import ChainMap, defaultdict, Counter

from DiceStatistics import d, Dice

#@profile
def comb(outcomes, inpt, func, mem):
	"""
	when 2 dice are the same it gives the wrong resault	

	optimization: 
	if dice_mask as multiple hits, then we can just combine
	their count, and then continue down without
	this current outcome.
	example:
		dice_mask = which_dice(inpt, outcome)
		c = [d[outcome] for d in compress(inpt,dice_mask)]
		res = comb(outcomes[i+1], left_over, func)
		#construct solution
	so we can ignore the dice loop
	
	2)
	i could maybe have a function that finds the next outcome from
	the remaining dice. So i can skip calls
	"""
	cache_key = tuple(inpt)
	if cache_key in mem:
		return mem[cache_key]
	if not outcomes or not inpt:
		return {}
	
	res = defaultdict(int)
	for i, outcome in enumerate(outcomes):
		for idx, die in enumerate(inpt):
			if not outcome in die:
				continue
			c = die[outcome]
			sub_bag = inpt.copy()
			sub_bag.pop(idx)
			if sub := comb(outcomes, sub_bag, func, mem):
				for sf, sc in sub.items():
					res[func(outcome,sf)] += sc*c
			else:
				res[outcome] = c
	mem[cache_key] = res
	return res
		




import time
n = 2
a = d(2)
inpt = [a]*n
inpt = [
	Dice.from_dict({1:1,2:1}),
	Dice.from_dict({1:1,2:1})
]
outcomes = sorted(list(ChainMap(*inpt)),reverse=True)
print(outcomes)
mem = {}
t = time.time()
res = comb(outcomes, inpt, lambda x,y: x+y, mem)
print("time = ", time.time() - t)
dice = Dice.from_dict(res)
print(res)
print(dice)
#print(dice.p)

#res = dict(sorted(res.items(), key = lambda x: x[0]))
#print(Dice.from_dict(res))
#print(n@a)
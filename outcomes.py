#from line_profiler import profile
from itertools import compress
from collections import ChainMap, defaultdict

from DiceStatistics import d, Dice

#@profile
def which(inpt, outcome):
	
	return [(outcome in i) for i in inpt]


CALLS = 0
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

	"""
	global CALLS
	CALLS += 1

	cache_key = tuple(inpt)
	if cache_key in mem:
		return mem[cache_key]
	if not outcomes or not inpt:
		return {}
	
	res = defaultdict(int)
	for i, outcome in enumerate(outcomes):
		#dice_mask = which(inpt, outcome)
		#for idx, (die, mask) in enumerate(zip(inpt, dice_mask)): # same as list[mask] in numpy
		#	if not mask:
		#		continue
		for idx, die in enumerate(inpt):
			if not outcome in die:
				continue
			c = die[outcome]
			left_over = [v for i, v in enumerate(inpt) if i != idx]# the problem! i != die, is problematic if the dice has the same hash, is not is problematic if the dice is copies eg [a]*5
			if sub := comb(outcomes, left_over, func, mem):
				for sf, sc in sub.items():
					res[func(outcome,sf)] += sc*c
			else:
				res[outcome] = c
	mem[cache_key] = res
	return res
		




import time
n = 17
a = d(50)
inpt = [a]*n
outcomes = sorted(list(ChainMap(*inpt)),reverse=True)
print(outcomes)
mem = {}
t = time.time()
res = comb(outcomes, inpt, lambda x,y: x+y, mem)
print("time = ", time.time() - t)
dice = Dice.from_dict(res)
print(CALLS)
#print(dice)

#res = dict(sorted(res.items(), key = lambda x: x[0]))
#print(Dice.from_dict(res))
#print(n@a)
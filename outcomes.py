from itertools import compress
from collections import ChainMap, defaultdict

from DiceStatistics import d, Dice

def which_dice(inpt, outcome):
	return [(outcome in i) for i in inpt]



def comb(outcomes, inpt, func):
	"""
	optimization: 
	if dice_mask as multiple hits, then we can just combine
	their count, and then continue down without
	this current outcome

	"""
	if not outcomes or not inpt:
		return {}
	
	res = defaultdict(int)
	for i, outcome in enumerate(outcomes):
		dice_mask = which_dice(inpt, outcome)
		
		for die in compress(inpt, dice_mask): # same as list[mask] in numpy
			c = die[outcome]
			left_over = [i for i in inpt if i != die]
			if sub := comb(outcomes, left_over, func):
				for sf, sc in sub.items():
					res[func(outcome,sf)] += sc*c
			else:
				res[outcome] = c
	return res
		




a = Dice.from_dict({1:1,2:1,3:1})
b = Dice.from_dict({1:1,3:1})
c = Dice.from_dict({3:1, 4:1})
inpt = [a,b,c]
outcomes = sorted(list(ChainMap(*inpt)),reverse=True)
res = comb(outcomes, inpt, lambda x,y: x+y)
res = dict(sorted(res.items(), key = lambda x: x[0]))
print(Dice.from_dict(res))
print(a+b+c)
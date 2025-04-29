from itertools import product
from collections import defaultdict
from math import prod
from DiceStatistics._math import unique
from DiceStatistics._inpt_cleaning import sort_dict
import DiceStatistics.Dice as dice

type Dice = dice
type Pool = Pool


def add_outcomes(out, dice: list[Dice]):
	res = []
	if not out:
		for f in dice:
			res.append([f])
	else :
		for i in out:
			for f in dice:
				res.append(i+[f])
	return res

def generate_outcomes(dice):
	out = []
	for die in dice:
		out = add_outcomes(out, die)
	return [sorted(outcome) for outcome in out]

def unique_collapse(ls: list[Dice]):
	res: defaultdict[int] = defaultdict(int)
	for d in ls:
		for f, c in d.items():
			res[f] += c
	
	return sort_dict(res)

# Pool needs to be invoked in the interface witha  decorator, in which
# it is loaded with dice and the operations that needs to happen
class Pool(object):

	def __init__(self, dice: list[Dice | Pool]):
		self._bag = dice
		self._outcomes = unique_collapse(dice)

	def __iter__(self):
		#for i in product(*self._bag):
		#	yield sorted(i)
		res: defaultdict[int] = defaultdict(int)
		faces = [i.keys() for i in self._bag]
		counts = [i.values() for i in self._bag]
		for f, c in zip(product(*faces), product(*counts)):
			res[tuple(sorted(f))] += prod(c)
		return res.items()

		

	def __call__(self,func):
		def wrapper():
			#return dice(func(i) for i in self)
			return dice.from_dict({func(f):c for f,c in self})
		return wrapper


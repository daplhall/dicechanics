from itertools import product
from DiceStatistics._math import unique
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

# Pool needs to be invoked in the interface witha  decorator, in which
# it is loaded with dice and the operations that needs to happen
class Pool(object):

	def __init__(self, dice: list[Dice | Pool]):
		self._bag = dice

	def __iter__(self):
		for i in product(*self._bag):
			yield sorted(i)
				
	def __call__(self,func):
		def wrapper():
			return dice(func(i) for i in self)
		return wrapper


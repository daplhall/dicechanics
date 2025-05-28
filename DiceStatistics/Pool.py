from itertools import product
from collections import defaultdict
from math import prod
from DiceStatistics._math import unique
from DiceStatistics._inpt_cleaning import sort_dict
import DiceStatistics.Dice as dice
from DiceStatistics._dice_combinatorics import linear_non_selective

type Dice = dice.Dice
type Pool = Pool


# Pool needs to be invoked in the interface witha  decorator, in which
# it is loaded with dice and the operations that needs to happen
class Pool(object):

	def __init__(self, dice: list[Dice | Pool]):
		self._bag = dice

	def perform(self, func):
		res = linear_non_selective(self._bag, func)
		return dice.from_dict(res)

	def __call__(self,func):
		def wrapper():
			return self.perform(func)
		return wrapper
	


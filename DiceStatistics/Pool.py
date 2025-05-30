from itertools import product
from collections import defaultdict
from math import prod
from DiceStatistics._math import unique
from DiceStatistics._inpt_cleaning import sort_dict
import DiceStatistics.Dice as dice
from DiceStatistics._dice_combinatorics import linear_non_selective, linear_selective

type Dice = dice.Dice
type Pool = Pool


# Pool needs to be invoked in the interface witha  decorator, in which
# it is loaded with dice and the operations that needs to happen
class Pool(object):
	def __init__(self, dice: list[Dice | Pool]):
		self._bag = dice
		self._keep = None

	def perform(self, func):
		if self._keep is None or all(self._keep):
			res = linear_non_selective(self._bag, func)
		else:
			res = linear_selective(self._bag, self._keep, func)
		return dice.from_dict(res)
	
	def copy(self):
		res = Pool.__new__(Pool)
		res._bag = self._bag
		res._keep = self._keep
		return res

	
	def __getitem__(self, idx):
		res = self.copy()
		if isinstance(idx, slice):
			keep = [0]*len(self._bag)
			keep[idx] = [1]*len(keep[idx])
		else:
			keep = idx
		res._keep = keep
		return res

	def __call__(self,func):
		def wrapper():
			return self.perform(func)
		return wrapper

	def __add__(self, rhs: Dice | int | float | Pool):
		pass	
	


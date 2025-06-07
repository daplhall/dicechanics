from itertools import product
from collections import defaultdict
from math import prod
from DiceStatistics._math import unique
from DiceStatistics._inpt_cleaning import sort_dict
from DiceStatistics.Dice import Dice, convert_to_dice
from DiceStatistics._dice_combinatorics import linear_non_selective, linear_selective

# Pool needs to be invoked in the interface witha  decorator, in which
# it is loaded with dice and the operations that needs to happen
class Pool(object):
	def __init__(self, dice: list):
		self._bag = dice
		self._keep = None

	def perform(self, func):
		if self._keep is None or all(self._keep):
			res = linear_non_selective(self._bag, func)
		else:
			res = linear_selective(self._bag, self._keep, func)
		return Dice.from_dict(res)
	
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
	
	def __str__(self):
		n = len(self._bag)
		txt = "Pool(["
		for i, d in enumerate(self._bag):
			txt += str(d) + (", " if i < n - 1 else "")
		txt += "])"
		return txt
	
	def add_level2(self, rhs):
		res = self.copy()
		res._bag.append(rhs)
		return res
	
	def add_level3(self, rhs):
		res = self.copy()
		res._bag.extend(rhs._bag)
		return res
	
	def __add__(self, rhs):
		if isinstance(rhs, Pool):
			return self.add_level3(rhs)
		else:
			rhs = convert_to_dice(rhs)
			return self.add_level2(rhs)



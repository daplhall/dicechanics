from collections import defaultdict
from collections.abc import MutableMapping

import dicechanics as ds


def sort_dict(faces: MutableMapping) -> dict:
	"""
	Function that sorts a dictionary

	Parameters
	----------
	faces: dict
		The dict to be sorted.

	Returns
	-------
	out: dict
		The dict but sorted.
	"""
	return dict(sorted(faces.items(), key=lambda pair: pair[0]))


def expand_dice(data: dict) -> dict:
	"""
	Function that expands dice into a sequence of numbers.

	Parameters
	----------
	data: dict
		Dict of numbers and dict which are then expanded.
		Eg. [1,2,3,d4] -> [1,2,3,4]

	Returns
	-------
	out: dict
		A dict with the expanded values and data.
	"""
	dice = defaultdict(
		int, filter(lambda x: isinstance(x[0], ds.Die), data.items())
	)
	numbers = defaultdict(int, filter(lambda x: x[0] not in dice, data.items()))
	for i, die in enumerate(dice):
		for f in numbers.keys():
			numbers[f] *= die._units
		for d in dice:
			if d != die:
				dice[d] *= die._units
	for die, c in dice.items():
		for f, cd in die.items():
			numbers[f] += c * cd
	return numbers


def sort_expand(faces: dict) -> dict:
	"""
	Function that  sorts and exapnds a dictionary

	Parameters
	----------
	faces: dict
		Dict which represents the faces of a die. The face can itself
		be a die.

	Returns
	-------
	out: dict
		The expanded and sorted dict.

	"""
	return sort_dict(expand_dice(faces))

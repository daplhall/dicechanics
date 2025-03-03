
import DiceStatistics as ds
from collections import defaultdict
from DiceStatistics._math import unique

def sort_dict(faces: dict):
	return dict(sorted(faces.items(), key=lambda pair: pair[0]))

def expand_dice(data:dict)->defaultdict:
	"""
		expands dice in a dictionary, to a dict of numbers
	"""
	dice = defaultdict(
		int, 
		filter(lambda x: isinstance(x[0], ds.Dice), data.items())
	)
	numbers = defaultdict(
		int, 
		filter(lambda x: x[0] not in dice, data.items())
	)
	for i, die in enumerate(dice):
		for f in numbers.keys():
			numbers[f] *= die._units
		for d in dice:
			if d != die:
				dice[d] *= die._units
	for die, c in dice.items():
		for f, cd in die.items():
			numbers[f] += c*cd
	return numbers

def clean_faces(faces: dict) -> dict:
	faces = sort_dict(faces)
	return expand_dice(faces)

def collect_faces(faces: list) -> dict:
	faces = dict(zip(*unique(faces)))
	return clean_faces(faces)
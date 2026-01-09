from collections import defaultdict
from collections.abc import Iterable


def unique(array: Iterable):
	uniques = defaultdict(int)
	for e in array:
		uniques[e] += 1
	return uniques


def normalize(statisticalDict):
	norm = sum(statisticalDict.values())
	return {key: value / norm for key, value in statisticalDict.items()}


def sort_dict(faces):
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

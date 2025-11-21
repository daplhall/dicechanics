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

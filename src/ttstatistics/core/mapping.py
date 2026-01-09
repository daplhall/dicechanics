__all__ = ["GenericMapping", "expand"]

from collections import defaultdict

from ttstatistics.core import protocols


def expand(mapping: protocols.Mapping):
	dice = list(
		filter(
			lambda x: isinstance(x[0], (protocols.Mapping)),
			mapping.items(),
		)
	)
	numbers = defaultdict(
		lambda: 0,
		filter(
			lambda x: not isinstance(x[0], (protocols.Mapping)),
			mapping.items(),
		),
	)
	for die, dieProb in dice:
		mapping = die
		for face, prob in mapping.items():
			numbers[face] += prob * dieProb
	return numbers


class GenericMapping(protocols.Mapping):
	def __init__(self, data: protocols.Mapping = {}):
		self.internals = data

	def __bool__(self):
		return bool(self.internals)

	def items(self):
		return self.internals.items()

	def values(self):
		return self.internals.values()

	def keys(self):
		return self.internals.keys()

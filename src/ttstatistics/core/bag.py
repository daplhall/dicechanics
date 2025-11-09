from collections import defaultdict

from ttstatistics.core import protocols


class Bag(protocols.Bag):
	def __init__(self, data: dict[protocols.Mapping, int] = {}):
		self.internalMappings = data

	def keys(self):
		return self.internalMappings.keys()

	def values(self):
		return self.internalMappings.values()

	def items(self):
		return self.internalMappings.items()

	def __bool__(self):
		return bool(self.internalMappings)

	def __add__(self, rhs: protocols.Mapping | protocols.Bag):
		newMappings = defaultdict(int, self.items())
		if isinstance(rhs, protocols.Mapping):
			newMappings[rhs] += 1
		else:
			for key, val in rhs.items():
				newMappings[key] += val
		return type(self)(newMappings)

	def __len__(self):
		return len(self.internalMappings)

from collections import defaultdict

from ttstatistics.core import protocols
from ttstatistics.core.slice import Slice


class Bag(protocols.Bag):
	def __init__(self, data: dict[protocols.Mapping, int] = {}):
		self.internalMappings = data
		self.slice = None

	@classmethod
	def withSlice(cls, data, slicing):
		self = cls(data)
		self.slice = slicing
		return self

	def prepare(self):
		return self.internalMappings.items()

	def prepareSlice(self):
		return self.slice

	def __bool__(self):
		return bool(self.internalMappings)

	def __add__(self, rhs: protocols.Mapping | protocols.Bag):
		newMappings = defaultdict(int, self.items())
		if isinstance(rhs, protocols.Bag):
			for key, val in rhs.items():
				newMappings[key] += val
		else:
			newMappings[rhs] += 1
		return type(self)(newMappings)

	def __len__(self):
		return len(self.internalMappings)

	def __getitem__(self, item):
		if isinstance(item, slice):
			newSlice = Slice.fromSlice(item)
		elif isinstance(item, tuple):
			newSlice = Slice.fromList(list(item))
		else:
			raise TypeError("Wrong Type for getitem")

		return Bag.withSlice(self.internalMappings, newSlice)

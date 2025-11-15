__all__ = ["Group"]

from collections import defaultdict

from ttstatistics.core import protocols
from ttstatistics.core.slice import Slice


class Group(protocols.Group):
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

	def __add__(self, rhs: protocols.Mapping | protocols.Group):
		newMappings = defaultdict(int, self.items())
		if isinstance(rhs, protocols.Group):
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
		elif isinstance(item, (tuple, list)):
			newSlice = Slice.fromList(tuple(item))
		else:
			raise TypeError("Wrong Type for getitem")

		return type(self).withSlice(self.internalMappings, newSlice)

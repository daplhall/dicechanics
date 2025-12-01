__all__ = ["Group"]

from ttstatistics.core import protocols
from ttstatistics.core.slice import Slice


class Group(protocols.Group):
	def __init__(self, data: dict[protocols.Mapping, int] = {}):
		self.internalMappings = data
		self.slice = None

	def __hash__(self):
		return hash(tuple(self.internalMappings.items()) + (self.slice,))

	@classmethod
	def withSlice(cls, data, slicing):
		self = cls(data)
		if isinstance(slicing, slice):
			self.slice = Slice.fromSlice(slicing)
		else:
			self.slice = Slice.fromList(slicing)
		return self

	def prepare(self):
		return self.internalMappings.items()

	def prepareSlice(self):
		"""
		if isinstance(self.slice, slice):
			newSlice = Slice.fromSlice(self.slice)
		elif isinstance(self.slice, (tuple, list)):
			newSlice = Slice.fromList(tuple(self.slice))
		else:
			newSlice = self.slice
		"""
		return self.slice.copy() if self.slice is not None else self.slice

	def __bool__(self):
		return bool(self.internalMappings)

	def __eq__(self, rhs):
		return hash(self) == hash(rhs)

	def __getitem__(self, item):
		if isinstance(item, (tuple, list)):
			return self & item
		elif isinstance(item, int):
			return self & (item,)
		elif isinstance(item, slice):
			return type(self).withSlice(self.internalMappings, item)
		else:
			raise TypeError

	def _select(self, indexes, *, default):
		mask = [default] * sum(self.internalMappings.values())
		for i in indexes:
			mask[i] = not default
		return mask

	def __and__(self, rhs):
		return type(self).withSlice(
			self.internalMappings, self._select(rhs, default=False)
		)

	def __rand__(self, rhs):
		return self & rhs

	def __xor__(self, rhs):
		return type(self).withSlice(
			self.internalMappings, self._select(rhs, default=True)
		)

	def __rxor__(self, rhs):
		return self ^ rhs

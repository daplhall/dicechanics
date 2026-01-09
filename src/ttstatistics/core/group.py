__all__ = ["Group"]

from ttstatistics.core import protocols
from ttstatistics.core.slice import Slice


class Group(protocols.Group):
	"""
	Hello world
	"""

	def __init__(
		self, data: dict[protocols.Mapping, protocols.GroupCount] = {}
	):
		self.internalMappings = data
		self.slice = None

	def __hash__(self):
		return hash(tuple(self.internalMappings.items()) + (self.slice,))

	@classmethod
	def withSlice(cls, data, slicing):
		self = cls(data)
		if isinstance(slicing, slice):
			keep = [
				0
			] * sum(  # TODO This is also in select which we pass in, it smells
				max((c for c, _ in value))
				for value in self.internalMappings.values()
			)
			keep[slicing] = [1] * len(keep[slicing])
			slicing = keep
		self.slice = Slice.fromList(slicing)
		return self

	def prepare(self):
		return self.internalMappings.items()

	def prepareSlice(self):
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
		# mask = [default] * sum(self.internalMappings.values())
		mask = [default] * sum(
			max((c for c, _ in value))
			for value in self.internalMappings.values()
		)
		for i in indexes:
			if i < len(mask) and i >= -len(mask):
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

__all__ = ["GenericMapping"]

from ttstatistics.core import protocols


class GenericMapping(protocols.Mapping):
	def __init__(self, data: dict = {}):
		self.internals = data

	def __bool__(self):
		return bool(self.internals)

	def items(self):
		return self.internals.items()

	def values(self):
		return self.internals.values()

	def keys(self):
		return self.internals.keys()

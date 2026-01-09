from enum import IntEnum, auto

from ttstatistics.core import protocols


class VariableCount:
	"""
	# when included in a mapping it should always have 0 as properbility
	"""

	def __init__(self, mapping: protocols.Mapping):
		self.max = max(mapping.keys())
		self.counts = mapping
		# self.counts = {
		# (self.max - key): value for key, value in mapping.items()
		# }

	def __hash__(self):
		return hash(tuple(self.counts.items()))

	def __add__(self, other):
		return self.max + other

	def __radd__(self, other):
		return self + other


class GroupCountInt(protocols.GroupCount):
	def __init__(self, count: int):
		self._count = count

	def __hash__(self):
		return hash(self._count)

	def __iter__(self):
		yield self._count, 1

	@property
	def max(self):
		return self._count


class GroupCountMapping(protocols.GroupCount):
	def __init__(self, counts: protocols.Mapping):
		self._counts = counts

	def __hash__(self):
		return hash(tuple(self._counts.items()))

	def __iter__(self):
		yield from self._counts.items()

	@property
	def max(self):
		return max(self._counts.keys())


class GroupCountTypes(IntEnum):
	int = auto()
	mapping = auto()


class GroupCountFactory(protocols.GroupCountFactory):
	_creators: dict[GroupCountTypes, protocols.GroupCount] = {}

	@classmethod
	def register(cls, key: GroupCountTypes, builder: protocols.GroupCount):
		cls._creators[key] = builder

	def create(self, key: GroupCountTypes):
		creator = self._creators.get(key)
		if creator is None:
			raise TypeError(f"Type not supported for GroupCount - {type(key)}")
		return creator


GroupCountFactory.register(GroupCountTypes.int, GroupCountInt)
GroupCountFactory.register(GroupCountTypes.mapping, GroupCountMapping)

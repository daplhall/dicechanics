from ttstatistics.core.group import Group
from ttstatistics.dicechanics import protocols


class Pool(Group, protocols.Pool):
	def __init__(self, data: dict[protocols.Die, int] = {}):
		super().__init__(data)

	def extend(self, obj: protocols.Die) -> None:
		self.__updateInternals(obj, 1)

	def __add__(self, rhs: protocols.Pool) -> protocols.Pool:
		out = type(self)(self.internalMappings.copy())
		for die, count in rhs.internalMappings.items():
			out.__updateInternals(die, count)
		return out

	def __updateInternals(self, key: protocols.Die, amount: int) -> None:
		if key in self.internalMappings:
			self.internalMappings[key] += amount
		else:
			self.internalMappings[key] = amount

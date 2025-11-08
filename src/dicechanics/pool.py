from dicechanics import protocols


class Pool(protocols.Pool):
	def __init__(self, data: protocols.bag = {}):
		self._bag = data

	def peekInside(self):
		return self._bag

	def __bool__(self):
		return bool(self._bag)


"""
	def __init__(self, data: list[protocols.Mapping] = []):
		self._bag = data

	@classmethod
	def from_list(cls, data: list[protocols.Mapping]):
		return cls(data)

	@classmethod
	def from_mapping(cls, data: protocols.Mapping):
		return cls.from_list([data])

	def __bool__(self):
		return bool(self.bag)

	def __len__(self):
		return len(self.bag)

	def __add__(self, rhs: protocols.Pool | protocols.Mapping) -> "Pool":
		if isinstance(rhs, protocols.Mapping):
			return type(self).from_list(self.bag + [rhs])
		elif isinstance(self, protocols.Pool):
			return type(self).from_list(self.bag + rhs.bag)
		else:
			raise TypeError("Unsupported type")

	@property
	def bag(self):
		return self._bag
"""

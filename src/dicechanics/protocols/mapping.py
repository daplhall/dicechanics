from typing import Protocol, runtime_checkable


@runtime_checkable
class Mapping(Protocol):
	def __add__(self, rhs): ...

	@property
	def mean(self):
		return self.internalData.mean

	@property
	def varians(self):
		return self.internalData.varians

	@property
	def std(self):
		return self.internalData.std

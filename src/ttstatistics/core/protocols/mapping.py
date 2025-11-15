__all__ = ["Mapping"]

from typing import Protocol, runtime_checkable


@runtime_checkable
class Mapping(Protocol):
	def items(self): ...
	def keys(self): ...
	def values(self): ...

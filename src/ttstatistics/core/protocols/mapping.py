__all__ = ["Mapping"]

from numbers import Number
from typing import Protocol, runtime_checkable


@runtime_checkable
class Mapping[T, Number](Protocol):
	def items(self): ...
	def keys(self): ...
	def values(self): ...

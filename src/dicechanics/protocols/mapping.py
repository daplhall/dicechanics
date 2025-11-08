from collections.abc import Callable
from typing import Protocol, runtime_checkable


@runtime_checkable
class Mapping[T](Protocol):
	def __add__(self, rhs): ...

	def map(self, mapping: Callable[[T], T]): ...

	@property
	def mean(self): ...

	@property
	def varians(self): ...

	@property
	def std(self): ...

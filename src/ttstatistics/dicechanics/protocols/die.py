from collections.abc import Callable

from ttstatistics.core.protocols import Mapping


class Die[T](Mapping):
	def __add__(self, rhs): ...

	def map(self, mapping: Callable[[T], T]): ...

	@property
	def mean(self): ...

	@property
	def varians(self): ...

	@property
	def std(self): ...

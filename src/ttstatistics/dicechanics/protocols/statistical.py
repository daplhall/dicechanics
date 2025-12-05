from abc import abstractmethod
from collections.abc import Callable
from numbers import Number
from typing import Protocol, runtime_checkable

from ttstatistics.core import protocols


@runtime_checkable
class Statistical[T](Protocol):
	def items(self): ...
	def values(self): ...
	def keys(self): ...
	def map(self, mapping: Callable[[T], T]) -> "Statistical": ...
	@property
	@abstractmethod
	def mean(self): ...

	@property
	@abstractmethod
	def varians(self): ...

	@property
	@abstractmethod
	def std(self): ...


class StatisticalFactory[T](Protocol):
	@abstractmethod
	def create(self, data: protocols.Mapping[T, Number]): ...

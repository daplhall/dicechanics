from typing import Protocol, runtime_checkable

from ttstatistics.core import protocols


@runtime_checkable
class Collection(Protocol):
	groups: list[protocols.Group]

	def __bool__(self): ...

from typing import Protocol, runtime_checkable

from ttstatistics.core.protocols import Mapping


@runtime_checkable
class Pool(Protocol):
	bag: list[Mapping]

	def __bool__(self): ...

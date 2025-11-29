__all__ = ["Group", "Slice"]

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from ttstatistics.core.protocols.base import Unit

type GroupItems = list[tuple[Unit, int]]


@runtime_checkable
class Slice(Protocol):
	@classmethod
	def fromList(cls, mask: Sequence[bool]): ...
	@classmethod
	def fromSlice(cls, slice_: slice): ...
	def next(self) -> bool: ...
	def previous(self) -> bool: ...


@runtime_checkable
class Group(Protocol):
	def prepare(self) -> GroupItems: ...
	def prepareSlice(self) -> Slice | None: ...

	def __bool__(self): ...

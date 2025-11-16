__all__ = [
	"AddUnit",
	"SubUnit",
	"MulUnit",
	"DivUnit",
	"FloorDivUnit",
	"Unit",
	"InputFunction",
]

from collections.abc import Callable
from typing import Protocol, runtime_checkable


@runtime_checkable
class AddUnit(Protocol):
	def __add__(self, lhs): ...


@runtime_checkable
class SubUnit(Protocol):
	def __sub__(self, lhs): ...


@runtime_checkable
class MulUnit(Protocol):
	def __mul__(self, lhs): ...


@runtime_checkable
class DivUnit(Protocol):
	def __truediv__(self, lhs): ...


@runtime_checkable
class FloorDivUnit(Protocol):
	def __floordiv__(self, lhs): ...


type Unit = AddUnit | SubUnit | MulUnit | DivUnit | FloorDivUnit

type InputFunction = Callable[[Unit, Unit], Unit]

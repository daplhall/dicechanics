from typing import Protocol, runtime_checkable


@runtime_checkable
class Mapping(Protocol):
	def tmp(self): ...

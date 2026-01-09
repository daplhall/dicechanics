from typing import Protocol, runtime_checkable

from ttstatistics.core import protocols


## Should just be a generator
## usage for i in VariableCount:
@runtime_checkable
class GroupCount(Protocol):
	def __iter__(self): ...


@runtime_checkable
class GroupCountFactory(Protocol):
	def create(self, dtype: str): ...

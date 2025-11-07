from typing import Protocol, runtime_checkable

from dicechanics.protocols import Mapping


@runtime_checkable
class Pool(Protocol):
	bag: list[Mapping]

	def isEmpty(self):
		pass

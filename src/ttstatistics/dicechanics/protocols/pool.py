from __future__ import annotations

from ttstatistics.core.protocols.group import Group
from ttstatistics.dicechanics.protocols import Die


class Pool(Group):
	def extend(self, obj: Die) -> None: ...
	def __add__(self, rhs: Pool) -> Pool: ...

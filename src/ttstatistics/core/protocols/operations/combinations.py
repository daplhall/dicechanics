from typing import Protocol

from ttstatistics.core.protocols.base import InputFunction
from ttstatistics.core.protocols.group import Group
from ttstatistics.core.protocols.mapping import Mapping


class Combinations(Protocol):
	def calculate(self, group: Group, operations: InputFunction) -> Mapping: ...

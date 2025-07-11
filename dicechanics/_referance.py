from typing import Any


class Ref:
	def __init__(self, referenced_item: Any = None):
		self._ref = referenced_item

	def get(self):
		return self._ref

	def set(self, new_ref):
		self._ref = new_ref

	def __bool__(self):
		return self._ref is not None

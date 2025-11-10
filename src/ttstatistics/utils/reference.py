from typing import Any


class Reference:
	"""
	A Reference class, which acts like a pointer.
	None is use as NULL
	"""

	def __init__(self, referenced_item: Any):
		self._ref = referenced_item

	def get(self) -> Any:
		"""
		Returns the value references by the "pointer".

		Returns
		-------
		out: Any
			The object pointed to.
		"""
		return self._ref

	def set(self, new_ref: Any):
		"""
		Sets the value in the pointer
		"""
		self._ref = new_ref

	def __bool__(self):
		"""
		Evaluates if something is stored in the reference.
		"""
		return self._ref is not None

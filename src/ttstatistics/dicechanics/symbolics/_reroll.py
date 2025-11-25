__all__ = ["RerollSymbol", "reroll"]
from ttstatistics.core.operations import micro


class RerollSymbol:
	def __init__(self, data=None, *, depth=1):
		self.internals = data
		self.depth = depth

	def __bool__(self):
		return bool(self.internals)

	def _binary(self, rhs, operation):
		if self.internals is None:
			return type(self)(rhs)
		else:
			return type(self)(operation(self.internals, rhs))

	def __add__(self, rhs):
		return self._binary(rhs, micro.add)

	def __sub__(self, rhs):
		return self._binary(-rhs, micro.add)

	def __mul__(self, rhs):
		return self._binary(rhs, micro.mul)

	def __truediv__(self, rhs):
		return self._binary(rhs, micro.div)

	def __floordiv__(self, rhs):
		return self._binary(rhs, micro.floorDiv)


reroll = RerollSymbol()

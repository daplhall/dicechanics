import operator as ops
from collections import defaultdict
from itertools import product

from dicechanics.baseunits.statistical_unit import StatisticalUnit


class MathOpsUnit(StatisticalUnit):
	def __init__(self, data=None, /, **kwargs):
		super().__init__(data, **kwargs)

	def isequal(self, rhs):
		if issubclass(type(rhs), MathOpsUnit):
			return hash(self) == hash(rhs)
		else:
			return False

	def bin_lvl0(self, rhs, ops):
		return type(self)({ops(key, rhs): value for key, value in self.items()})

	def bin_lvl1(self, rhs, ops):
		res = defaultdict(int)
		for (k1, v1), (k2, v2) in product(self.items(), rhs.items()):
			res[ops(k1, k2)] += v1 * v2
		return type(self)(res)

	def bin_ops(self, rhs, ops):
		if issubclass(type(rhs), MathOpsUnit):
			return self.bin_lvl1(rhs, ops)
		else:
			return self.bin_lvl0(rhs, ops)

	def __add__(self, rhs):
		return self.bin_ops(rhs, ops.add)

	def __radd__(self, lhs):
		return self.bin_ops(lhs, ops.add)

	def __sub__(self, rhs):
		return self.bin_ops(rhs, ops.sub)

	def __rsub__(self, lhs):
		return (-self).bin_ops(lhs, ops.add)

	def __mul__(self, rhs):
		return self.bin_ops(rhs, ops.mul)

	def __rmul__(self, lhs):
		return self.bin_ops(lhs, ops.mul)

	def __truediv__(self, rhs):
		"""
		Return self / value
		"""
		return self.bin_op(rhs, ops.truediv)

	def __floordiv__(self, rhs):
		"""
		Return self // value
		"""
		return self.bin_ops(rhs, ops.floordiv)

	def __lt__(self, rhs):
		"""
		Return self < value
		"""
		return self.bin_ops(rhs, ops.lt)

	def __le__(self, rhs):
		"""
		Return self <= value
		"""
		return self.bin_ops(rhs, ops.le)

	def __ge__(self, rhs):
		"""
		Return self => value
		"""
		return self.bin_ops(rhs, ops.ge)

	def __gt__(self, rhs):
		"""
		Return self > value
		"""
		return self.bin_ops(rhs, ops.gt)

	def __eq__(self, rhs):
		"""
		Return self == value
		"""
		return self.is_equal(rhs)

	def __ne__(self, rhs):
		"""
		Return self != value
		"""
		return not self.is_equal(rhs)

	def unary(self, ops):
		return type(self)({ops(key): value for key, value in self.items()})

	def __neg__(self):
		"""
		Return -self
		"""
		return self.unary(ops.neg)

	def __pos__(self):
		"""
		Return +self
		"""
		return self.unary(ops.pos)

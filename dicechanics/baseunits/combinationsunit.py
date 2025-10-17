import operator as ops
from collections import defaultdict
from itertools import product

from dicechanics.baseunits.statisticalunit import StatisticalUnit


class CombinationsUnit(StatisticalUnit):
	"test"

	def __init__(self, data=None, /, **kwargs):
		"""
		Initializes the unit, its recommended to use :func:`d` interface.

		Parameters
		----------
		data: dict
			A dict as input
		"""
		super().__init__(data, **kwargs)

	def _isequal(self, rhs):
		"""
		Function that checks if equality of objects.
		If its not a Die object then it always return false.

		Parameters
		----------
		rhs: object
			The object thats we compare the unit to.

		Returns
		-------
		out: bool
			Bool representing if the object is equal to the unit.
		"""

		if issubclass(type(rhs), CombinationsUnit):
			return hash(self) == hash(rhs)
		else:
			return False

	def _bin_lvl0(self, rhs, ops):
		"""
		Function for binary level 0 operations between the die and @rhs

		Parameters
		----------
		rhs: object
			The object which the die needs to operate with
		ops: Callable
			The operator which acts on rhs and the die

		Returns
		-------
		out: type(self)
			A new unit representing the operation between original die
			and rhs
		"""

		retrn = defaultdict(int)
		for key, value in self.items():
			retrn[ops(key, rhs)] += value
		return type(self)(retrn)

	def _bin_lvl1(self, rhs, ops):
		"""
		Function for binary level 1 operations between the unit and @rhs

		Parameters
		----------
		rhs: object
			The other die which the self needs to operate with
		ops: Callable
			The operator which acts on rhs and the unit

		Returns
		-------
		out: type(self)
			A new unit representing the operation between original unit
			and rhs
		"""
		res = defaultdict(int)
		for (k1, v1), (k2, v2) in product(self.items(), rhs.items()):
			res[ops(k1, k2)] += v1 * v2
		return type(self)(res)

	def _bin_ops(self, rhs, ops):
		"""
		Function that performs binary operations between the unit and @rhs

		Parameters
		----------
		rhs: object
			The object which the unit needs to operate with
		ops: Callable
			The operator which acts on rhs and the unit

		Returns
		-------
		out: type(self)
			A new unit representing the operation between original unit
			and rhs
		"""
		if issubclass(type(rhs), CombinationsUnit):
			return self._bin_lvl1(rhs, ops)
		else:
			return self._bin_lvl0(rhs, ops)

	def __add__(self, rhs):
		"""
		Return self + value
		"""
		return self._bin_ops(rhs, ops.add)

	def __radd__(self, lhs):
		"""
		Return value + self
		"""
		return self._bin_ops(lhs, ops.add)

	def __sub__(self, rhs):
		"""
		Return self - value
		"""
		return self._bin_ops(rhs, ops.sub)

	def __rsub__(self, lhs):
		"""
		Return value - self
		"""
		return (-self)._bin_ops(lhs, ops.add)

	def __mul__(self, rhs):
		"""
		Return value * self
		"""
		return self._bin_ops(rhs, ops.mul)

	def __rmul__(self, lhs):
		"""
		Return self / value
		"""
		return self._bin_ops(lhs, ops.mul)

	def __truediv__(self, rhs):
		"""
		Return self / value
		"""
		return self._bin_ops(rhs, ops.truediv)

	def __floordiv__(self, rhs):
		"""
		Return self // value
		"""
		return self._bin_ops(rhs, ops.floordiv)

	def __lt__(self, rhs):
		"""
		Return self < value
		"""
		return self._bin_ops(rhs, ops.lt)

	def __le__(self, rhs):
		"""
		Return self <= value
		"""
		return self._bin_ops(rhs, ops.le)

	def __ge__(self, rhs):
		"""
		Return self => value
		"""
		return self._bin_ops(rhs, ops.ge)

	def __gt__(self, rhs):
		"""
		Return self > value
		"""
		return self._bin_ops(rhs, ops.gt)

	def __eq__(self, rhs):
		"""
		Return self == value
		"""
		return self._isequal(rhs)

	def __ne__(self, rhs):
		"""
		Return self != value
		"""
		return not self._isequal(rhs)

	def _unary(self, ops):
		"""
		Function for applying level 0 unary operations to self

		Parameters
		----------
		ops:Callable
			The unary ops

		Returns
		-------
		out: type(self)
			The new die representing the operation
		"""
		return type(self)({ops(key): value for key, value in self.items()})

	def __neg__(self):
		"""
		Return -self
		"""
		return self._unary(ops.neg)

	def __pos__(self):
		"""
		Return +self
		"""
		return self._unary(ops.pos)

	def __hash__(self):
		return super().__hash__()

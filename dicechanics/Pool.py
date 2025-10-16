__all__ = ["Pool"]

from numbers import Number

from dicechanics._dice_combinatorics import (
	linear_non_selective,
	linear_selective,
)
from dicechanics._typing import BinaryFunc_T
from dicechanics.Die import Die


def convert_to_die(inpt: object):
	if isinstance(inpt, Number):
		return Die({inpt: 1})
	elif isinstance(inpt, Die):
		return inpt
	else:
		raise ValueError("Inpt is not a primitive or a Die")


# Pool needs to be invoked in the interface witha  decorator, in which
# it is loaded with dice and the operations that needs to happen
class Pool:
	"""
	Class that represents a pool of dice."""

	def __init__(self, dice: list):
		"""
		Initializes the pool.It is recommend to use :func:`pool`
		interface.
		"""
		self._bag = dice
		self._keep = None

	def perform(self, func: BinaryFunc_T) -> Die:
		"""
		Function that applies a given function to the elements in the pool.
		The function must have the form f(x, y)	-> z, and its operation
		must be linear, ie. the order in which the values are calculated
		doesn't matter.

		Parameters
		----------
		func: Callable
			Function with the form f(x, y) -> z. It must apply a linear
			operation

		Returns
		-------

		"""
		if self._keep is None or all(self._keep):
			res = linear_non_selective(self._bag, func)
		else:
			res = linear_selective(self._bag, self._keep, func)
		return res

	def copy(self):
		"""
		Function that creates a copy of the pool

		Returns
		-------
		out: Pool
			A copy of the current pool
		"""
		res = Pool(self._bag)
		res._keep = self._keep
		return res

	def __getitem__(self, idx):
		"""
		Get in this function defines which faces in sorted outcomes of
		rolling the back needs to be selected and operated on in the perform
		method

		Parameters
		----------
		idx: list | slice

		Returns
		-------
		out: pool
			A pool copy with which die to keep set
		"""
		res = self.copy()
		if isinstance(idx, slice):
			keep = [0] * len(self._bag)
			keep[idx] = [1] * len(keep[idx])
		else:
			keep = idx
		res._keep = keep
		return res

	def __call__(self, func):
		"""
		A wrapper for perform, allows the pool to be used as a decorator
		"""

		def wrapper():
			return self.perform(func)

		return wrapper

	def __repr__(self):
		n = len(self._bag)
		txt = "Pool(["
		for i, d in enumerate(self._bag):
			txt += repr(d) + (", " if i < n - 1 else "")
		txt += "])"
		return txt

	def __str__(self):
		return repr(self)

	def _add_level2(self, rhs):
		"""
		Function that applies lvl 2 operations to the pool

		Parameters
		----------
		rhs: die | float
			The value to be added to the bag

		Returns
		-------
		out: pool
			A new pool with the added input
		"""
		res = self.copy()
		res._bag.append(rhs)
		return res

	def _add_level3(self, rhs):
		"""
		Function that applies lvl 3 operations to the pool

		Parameters
		----------
		rhs: pool
			The pool that needs to extend the current pool

		Returns
		-------
		out: pool
			A new pool with the added input
		"""
		res = self.copy()
		res._bag.extend(rhs._bag)
		return res

	def __add__(self, rhs):
		"""
		Return self + value
		"""
		if isinstance(rhs, Pool):
			return self._add_level3(rhs)
		else:
			rhs = convert_to_die(rhs)
			return self._add_level2(rhs)

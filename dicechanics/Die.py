__all__ = ["Die"]

import operator as op
import warnings as wa
from collections import defaultdict
from collections.abc import ItemsView, KeysView, ValuesView
from itertools import product
from math import sqrt
from typing import Any, Callable, Generator, Iterable

from dicechanics._inpt_cleaning import (
	clean_faces,
	collect_faces,
	expand_dice,
	sort_dict,
)
from dicechanics._math import gcd
from dicechanics._strplot import str_plot
from dicechanics._typing import BinaryFunc_T, CompareFunc_T, UnaryFunc_T
from dicechanics.ParamChecker import ParamChecker

type Die_T = Die
type PureFunc_T = Callable[[Any], Any]

PRIMITIVES = (float, int)
PLOT_WIDTH = 20


@ParamChecker
def die_map_template(outcome):
	pass


def DieFunction(func):
	ParamChecker.check(func)
	return func


def convert_to_die(inpt: object) -> Die_T:
	if isinstance(inpt, PRIMITIVES):
		return Die([inpt])
	elif isinstance(inpt, Die):
		return inpt
	else:
		raise ValueError("Inpt is not a primitive or a Die")


class Die:
	"""
	The class that represents a statistical presentation of a die.
	"""

	def __init__(
		self, faces: Iterable[float], /, rounding: PureFunc_T = lambda x: x
	):
		"""
		Initializes the Die, its recommended to use :func:`d` interface.
		"""
		self._data = collect_faces(faces)
		self._derived_attr()
		self._rounding = rounding

	@classmethod
	def from_dict(cls, data: dict[object, int], rounding=lambda x: x) -> Die_T:
		"""
		Constructor that creates a die directly from a dict.

		Parameters
		----------
		data: dict
			The data in the form of a dict.
		rounding: Callable
			A function that determines how to round outcomes.

		Returns
		-------
		out: Die
		"""
		self = cls.__new__(cls)
		self._data = clean_faces(data)
		self._derived_attr()
		self._rounding = rounding
		return self

	def _derived_attr(self):
		"""
		A helper function that sets all derived stats.

		Returns
		-------
		out: None
		"""
		self._simplify()
		self._units = sum(self._data.values())
		self._p = [i / self._units for i in self.c]
		self._mean = sum(p * f for p, f in zip(self.p, self.f))
		self._var = sum(
			p * (x - self._mean) ** 2 for x, p in zip(self.f, self.p)
		)
		self._hash = hash(tuple(self._data.items()) + (self._mean,))
		self._cdf = self._cumulative()
		self._max = max(self._data)
		self._min = min(self._data)

	def _cumulative(self) -> list[float]:
		"""
		Function that calculates the cumulative probability of the Die.

		Returns
		-------
		out: list
			The cumulative probability
		"""
		out: list[float] = []
		for p in self.p:
			out.append(p + out[-1] if out else p)
		return out

	def _simplify(self):
		"""
		Helper function that simplifies the data.

		Returns
		-------
		out: None
		"""
		c = self.c
		if len(c) > 1:
			d = gcd(c[0], c[1])
			for i in c[2:]:
				d = gcd(d, i)
				if d == 1:
					break
			self._data = {f: c // d for f, c in self.items()}

	@property
	def f(self) -> list:
		"""
		Returns the faces of the die

		Returns
		-------
		out: list
			The faces of the die.
		"""
		return list(self._data.keys())

	@property
	def nfaces(self) -> int:
		"""
		Returns the number of faces a physical die needs to represent
		this die.

		Returns
		-------
		out: int
			Number of faces needed to present this die as a physical die.
		"""
		return self._units

	@property
	def p(self) -> list:
		"""
		Returns the probability of the die

		Returns
		-------
		out: list
			The probability of the die.
		"""
		return self._p

	@property
	def c(self) -> list:
		"""
		Returns the count list of the die

		Returns
		-------
		out: list
			The number pr face of the die.
		"""
		return list(self._data.values())

	@property
	def mean(self) -> float:
		"""
		Returns the mean of the die

		Returns
		-------
		out: float
			The mean of the die.
		"""
		return self._mean

	@property
	def cdf(self) -> list:
		"""
		Returns the cumulative probability of the die

		Returns
		-------
		out: List
			The cumulative probability of the die.
		"""
		return self._cdf

	@property
	def var(self) -> float:
		"""
		Returns the variance of the die

		Returns
		-------
		out: float
			The variance of the die.
		"""
		return self._var

	@property
	def std(self) -> float:
		"""
		Returns the standard deviation of the die

		Returns
		-------
		out: float
			The standard deviations of the die.
		"""
		return sqrt(self._var)

	def max(self) -> float:
		"""
		Returns the maximum face of the die.

		Parameters
		-------
		out: float
			The maximum face of the die.
		"""
		return self._max

	def min(self) -> float:
		"""
		Returns the minimum faces of the die

		Parameters
		-------
		out: float
			The minimum face of the die
		"""
		return self._min

	def copy(self) -> Die_T:
		"""
		Function that creates a copy of the die

		Returns
		-------
		out: Die
			The copy
		"""
		return Die.from_dict(self._data)

	def keys(self) -> KeysView:
		"""
		Get the keys of the internal dict.

		Returns
		-------
		out: KeysView
			The keys if the internal data.
		"""
		return self._data.keys()

	def values(self) -> ValuesView:
		"""
		Get the values of the internal dict.

		Returns
		-------
		out: ValuesView
			The values if the internal data.
		"""
		return self._data.values()

	def items(self) -> ItemsView:
		"""
		Get the items (keys and values) of the internal dict.

		Returns
		-------
		out: ValuesView
			The items if the internal data.
		"""
		return self._data.items()

	def reroll(self, *redo, depth: int | str = 1) -> Die_T:
		"""
		Function that rerolls on a given set of values

		Parameters
		----------
		*redo
			Faces to reroll
		depth: int | str
			the number of rerolls allowed. Inf for an infinite amount of times

		Returns
		out: Die
			A die that represents the rerolled probabilities
		-------
		"""
		if depth == "inf":
			return Die(i for i in self if i not in redo)
		faces = self._data
		for _ in range(depth):
			numbers = {f: c for f, c in faces.items() if f not in redo}
			dice = {self: sum(c for f, c in faces.items() if f in redo)}
			faces = expand_dice(numbers | dice)
		return Die.from_dict(sort_dict(faces))

	def _plode(self, ops: BinaryFunc_T, *ploder, depth: int = 1) -> Die_T:
		"""
		Function that handles actions in which you reroll the die, then
		on the reroll face you do an operation between the reroll and the
		reroll face

		Parameters
		----------
		ops: callable
			The operation; it is assumed that the face is first
			ie. ops(f, die)
		*ploder
			The numbers that need to be rerolled
		depth: int
			How many times do we reroll

		Returns
		-------
		out: Die
			A die representing the operation
		"""
		faces = self._data
		if depth > 0:
			numbers = {f: c for f, c in faces.items() if f not in ploder}
			dice = {
				(ops(f, self._plode(ops, *ploder, depth=depth - 1))): c
				for f, c in faces.items()
				if f in ploder
			}
			faces = expand_dice(numbers | dice)
		return Die.from_dict(sort_dict(faces))

	def explode(self, *exploder, depth: int = 1) -> Die_T:
		"""
		Function that explodes the die.
		Ie. Reroll on a value and add it to the rolled face.

		Parameters
		----------
		*exploder
			The numbers that need to be rerolled
		depth: int
			How many times do we reroll

		Returns
		-------
		out: Die
			A die representing the operation
		"""
		return self._plode(op.add, *exploder, depth=depth)

	def implode(self, *imploder, depth: int = 1) -> Die_T:
		"""
		Function that implodes the die.
		Ie. Reroll on a value and sub it from the rolled face.

		Parameters
		----------
		*imploder
			The numbers that need to be rerolled
		depth: int
			How many times do we reroll

		Returns
		-------
		out: Die
			A die representing the operation
		"""
		return self._plode(op.sub, *imploder, depth=depth)

	def count(self, *count) -> Die_T:
		"""
		Function that counts the given number of faces
		results in a true or false die

		Parameters
		----------
		count: args
			The faces we want to count

		Returns
		-------
		out: Die
			The die representing the operation
		"""
		return Die(i in count for i in self)

	def is_equal(self, rhs: object) -> bool:
		"""
		Function that checks if equality of objects.
		If its not a Die object then it always return false.

		Parameters
		----------
		rhs: object
			The object thats we compare the die to.

		Returns
		-------
		out: bool
			Bool representing if the object is equal to the die.
		"""
		if not isinstance(rhs, Die):
			return False
		else:
			return self._hash == rhs._hash

	def folding(self, rhs: object, ops: CompareFunc_T, into: object) -> Die_T:
		"""
		Function that takes values of the die, that are evaluated true
		when compared with @rhs through @ops. It them puts the counts into the
		value defined by @into

		Parameters
		----------
		rhs: object
			The object we compare in relation to
		ops: Callable
			The comparison operation
		into: object
			Where we store the evaluated numbers

		Returns
		-------
		out: Die
			The new die that with the values folded into @into
		"""
		data = defaultdict(
			int, {f: c for f, c in self.items() if not ops(f, rhs)}
		)
		c = sum(c for f, c in self.items() if ops(f, rhs))
		data[into] += c
		return Die.from_dict(data)

	def fold_over(self, rhs: object, /, into: object = None) -> Die_T:
		"""
		Function that folds values over @rhs and puts them into @into

		Parameters
		----------
		rhs: object
			The object we compare in relation to
		into: object
			Where we store the evaluated numbers

		Returns
		-------
		out: Die
			The new die that with the values folded into @into
		"""
		return self.folding(rhs, op.gt, into=rhs if into is None else into)

	def fold_under(self, rhs: object, /, into: object = None) -> Die_T:
		"""
		Function that folds values under @rhs and puts them into @into

		Parameters
		----------
		rhs: object
			The object we compare in relation to
		into: object
			Where we store the evaluated numbers

		Returns
		-------
		out: Die
			The new die that with the values folded into @into
		"""
		return self.folding(rhs, op.lt, into=rhs if into is None else into)

	def map(self, func: PureFunc_T) -> Die_T:
		"""
		Maps a function onto the die

		Parameters
		----------
		func: Callable
			The function to be mapped

		Returns
		-------
		out: Die
			The die with the results of the mapping
		"""
		return Die(func(i) for i in self)

	def __hash__(self) -> int:
		"""
		The hashing method
		"""
		return self._hash

	def __call__(self, func: PureFunc_T) -> Callable:
		"""
		Used to wrap die in as a decorator. It used the map function.

		Parameters
		----------
		func:
			The function to wrap.

		Returns
		-------
		out: callable
			A function that returns a die of the mapped function
		"""
		die_map_template.check(func)

		def wrapper():
			return self.map(func)

		return wrapper

	def __iter__(self) -> Generator:  # might need ot be text also when mask
		for f, c in self.items():
			for _ in range(c):
				yield f

	def __contains__(self, value: object) -> bool:
		return value in self._data.keys()

	def _binary_level0(self, rhs: object, ops: BinaryFunc_T) -> Die_T:
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
		out: Die
			A new die representing the operation between original die
			and rhs
		"""
		data = defaultdict[object, int](int)
		for f, c in self.items():
			key = self._rounding(ops(f, rhs))
			data[key] += c
		return Die.from_dict(data)

	def _binary_level1(self, rhs: Die_T, ops: BinaryFunc_T):
		"""
		Function for binary level 1 operations between the die and @rhs

		Parameters
		----------
		rhs: object
			The other die which the self needs to operate with
		ops: Callable
			The operator which acts on rhs and the die

		Returns
		-------
		out: Die
			A new die representing the operation between original die
			and rhs
		"""
		data = defaultdict[object, int](int)
		for (f1, c1), (f2, c2) in product(self.items(), rhs.items()):
			key = self._rounding(ops(f1, f2))
			data[key] += c1 * c2
		return Die.from_dict(data)

	def _binary_op(self, rhs: object, ops: BinaryFunc_T):
		"""
		Function that performs binary operations between the die and @rhs

		Parameters
		----------
		rhs: object
			The object which the die needs to operate with
		ops: Callable
			The operator which acts on rhs and the die

		Returns
		-------
		out: Die
			A new die representing the operation between original die
			and rhs
		"""
		if isinstance(rhs, Die):
			return self._binary_level1(rhs, ops)
		else:
			return self._binary_level0(rhs, ops)

	def __add__(self, rhs: object) -> Die_T:
		"""
		Return self + value
		"""
		return self._binary_op(rhs, op.add)

	def __radd__(self, lhs: object) -> Die_T:
		"""
		Return value + self
		"""
		return self._binary_op(lhs, op.add)

	def __sub__(self, rhs: object) -> Die_T:
		# needs to react to rounding
		"""
		Return self - value
		"""
		return self._binary_op(rhs, op.sub)

	def __rsub__(self, lhs: object) -> Die_T:
		"""
		Return value - self
		"""
		return (-self)._binary_op(lhs, op.add)

	def __mul__(self, rhs: object) -> Die_T:
		"""
		Return self * value
		"""
		# Needs to react to rounding
		return self._binary_op(rhs, op.mul)

	def __rmul__(self, lhs: object) -> Die_T:
		"""
		Return value * self
		"""
		return self._binary_op(lhs, op.mul)

	def __truediv__(self, rhs: object) -> Die_T:
		"""
		Return self / value
		"""
		# needs to reach to rounding
		return self._binary_op(rhs, op.truediv)

	def __floordiv__(self, rhs: object) -> Die_T:
		"""
		Return self // value
		"""
		# needs to reach to rounding
		return self._binary_op(rhs, op.floordiv)

	def __lt__(self, rhs: object) -> Die_T:
		"""
		Return self < value
		"""
		return self._binary_op(rhs, op.lt)

	def __le__(self, rhs: object) -> Die_T:
		"""
		Return self <= value
		"""
		return self._binary_op(rhs, op.le)

	def __ge__(self, rhs: object) -> Die_T:
		"""
		Return self => value
		"""
		return self._binary_op(rhs, op.ge)

	def __gt__(self, rhs: object) -> Die_T:
		"""
		Return self > value
		"""
		return self._binary_op(rhs, op.gt)

	def __eq__(self, rhs: object) -> bool:
		"""
		Return self == value
		"""
		return self.is_equal(rhs)

	def __ne__(self, rhs: object) -> bool:
		"""
		Return self != value
		"""
		return not self.is_equal(rhs)

	def _rolln_level0(self, lhs: int, ops: BinaryFunc_T) -> Die_T:
		"""
		Function for rolling self lhs times.

		Parameters
		----------
		lhs: int
			The number of times we roll the die
		ops: Callable
			The operation between the die.

		Returns
		-------
		out: Die
			The new die
		"""
		if lhs == 0:
			wa.warn("A 0d have been rolled", RuntimeWarning)
			return Die([0])
		if neg := lhs < 0:
			lhs *= -1
		res = self
		for _ in range(lhs - 1):
			res = ops(res, self)
		return -res if neg else res

	def _rolln_level1(self, lhs: Die_T, ops: BinaryFunc_T) -> Die_T:
		"""
		Function for rolling self n times, where n is a value in lhs.

		It overlaps the different results with each other.

		Parameters
		----------
		lhs: Die
			The die which indicates how many of self we roll
		ops: Callable
			The operation between the die.

		Returns
		-------
		out: Die
			The new die representing the operation
		"""
		dice = defaultdict(int)
		for f, c in self.items():
			die = lhs._binary_rolln(f, ops)
			dice[die] += c
		return Die.from_dict(dice)

	def _binary_rolln(self, lhs: int, ops: BinaryFunc_T) -> Die_T:
		"""
		Function for applying binary operations in which you roll self
		lhs times

		Parameters
		----------
		lhs: Die
			The die which indicates how many of self we roll
		ops: Callable
			The operation between the die.

		Returns
		-------
		out: Die
			The new die representing the operation
		"""
		if isinstance(lhs, int):
			return self._rolln_level0(lhs, ops)
		elif isinstance(lhs, Die):
			return self._rolln_level1(lhs, ops)
		else:
			raise ValueError("Unexpected type in dice matmul")

	def __rmatmul__(self, lhs: int) -> Die_T:
		"""
		Return value @ self
		"""
		return self._binary_rolln(lhs, op.add)

	def __matmul__(self, rhs) -> Die_T:
		"""
		Return self @ value
		if value is a Die then we roll that depending on the values in self
		"""
		return self._binary_rolln(rhs, op.add)

	def _unary_level0(self, ops: UnaryFunc_T) -> Die_T:
		"""
		Function for applying level 0 unary operations to self

		Parameters
		----------
		ops:Callable
			The unary ops

		Returns
		-------
		out: Die
			The new die representing the operation
		"""
		return Die(self._rounding(ops(i)) for i in self)

	def __neg__(self) -> Die_T:
		"""
		Return -self
		"""
		return self._unary_level0(op.neg)

	def __pos__(self) -> Die_T:
		"""
		Return +self
		"""
		return self._unary_level0(op.pos)

	def __getitem__(self, i) -> Die_T:
		return self.p[i]

	def __repr__(self) -> str:
		return "Die(" + str(self._data) + ")"

	def __str__(self) -> str:
		res = f"Die with mu - {self.mean:.2f}, sigma - {self.std:.2f}, faces - {self.nfaces}\n"  # noqa: E501h
		res += "-" * (len(res) - 1) + "\n"
		return res + str_plot(self, PLOT_WIDTH)

import operator as ops
import warnings as wa
from collections import defaultdict
from numbers import Number

from dicechanics._strplot import str_plot
from dicechanics.baseunits.combinationsunit import CombinationsUnit

PLOT_WIDTH = 20


class DieUnit(CombinationsUnit):
	"""test"""

	def __init__(self, data=None, /, **kwargs):
		super().__init__(self._expand(data), **kwargs)
		self.sort()
		self.simplify()

	@property
	def faces(self):
		"""
		Mirror for self.outcomes, that translates outcomes to faces
		"""
		return self.outcomes

	f = faces

	def reroll(self, *redo, depth=1):
		"""
		Function that rerolls on a given set of values

		Parameters
		----------
		*redo
			Faces to reroll
		depth: int | str
			the number of rerolls allowed. "Inf" as a string for an infinite amount of times

		Returns
		out: Die
			A die that represents the rerolled probabilities
		-------
		"""
		if depth == "inf":
			return type(self)(
				{key: value for key, value in self.items() if key not in redo}
			)
		faces = self.copy()
		for _ in range(depth):
			numbers = {f: c for f, c in faces.items() if f not in redo}
			dice = {self: sum(c for f, c in faces.items() if f in redo)}
			faces = self._expand(numbers | dice)
		return type(self)(faces)

	def _plode(self, ops, *ploder, depth=1):
		"""
		Function that handles actions in which you reroll the unit.

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
		out: type(self)
			A die representing the operation
		"""
		faces = self.copy()
		if depth > 0:
			numbers = {f: c for f, c in self.items() if f not in ploder}
			dice = {
				(ops(f, self._plode(ops, *ploder, depth=depth - 1))): c
				for f, c in self.items()
				if f in ploder
			}
			faces = faces._expand(numbers | dice)
		return type(self)(faces)

	def explode(self, *exploder, depth=1):
		"""
		Function that explodes the units outcomes.

		Parameters
		----------
		*exploder
			The numbers that need to be rerolled
		depth: int
			How many times do we reroll

		Returns
		-------
		out: type(self)
			A unit representing the operation
		"""
		return self._plode(ops.add, *exploder, depth=depth)

	def implode(self, *imploder, depth=1):
		"""
		Function that implodes the unit outcomes.

		Parameters
		----------
		*imploder
			The numbers that need to be rerolled
		depth: int
			How many times do we reroll

		Returns
		-------
		out: type(self)
			A unit representing the operation
		"""
		return self._plode(ops.sub, *imploder, depth=depth)

	def count(self, *targets):
		"""
		Function that counts the given number of outcomes, results in a binary unit

		Parameters
		----------
		count: args
			The faces we want to count

		Returns
		-------
		out: type(self)
			The unit representing the operation
		"""
		return self.map(lambda x: x in targets)

	def _folding(self, rhs, ops, into):
		"""
		Function that takes outcomes of the unit that are evaluated true,
		when compared with @rhs through @ops. It them puts the counts of those
		into the value defined by @into

		Parameters
		----------
		rhs: object>
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
		return type(self)(data)

	def fold_over(self, rhs, /, into=None):
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
		out: type(self)
			The new unit that with the values folded into @into
		"""
		return self._folding(rhs, ops.gt, into=rhs if into is None else into)

	def fold_under(self, rhs, /, into=None):
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
		out: type(self)
			The new unit that with the values folded into @into
		"""
		return self._folding(rhs, ops.lt, into=rhs if into is None else into)

	def _nrolls_lvl0(self, lhs, ops):
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
		out: type(self)
			The new unit
		"""
		if lhs == 0:
			wa.warn("A 0d have been rolled", RuntimeWarning)
			return type(self)({0: 1})
		if neg := lhs < 0:
			lhs *= -1
		res = self
		for _ in range(lhs - 1):
			res = ops(res, self)
		return -res if neg else res

	# can type(self) be formatted to be class.__name__?
	def _nrolls_lvl1(self, lhs, ops):
		"""
		Function for rolling self n times, where n is a value in lhs.

		It overlaps the different results with each other.

		Parameters
		----------
		lhs: type(self)
			The die which indicates how many of self we roll
		ops: Callable
			The operation between the die.

		Returns
		-------
		out: type(self)
			The new die representing the operation
		"""
		dice = defaultdict(int)
		for f, c in self.items():
			die = lhs._nrolls_lvl0(f, ops)
			dice[die] += c
		return type(self)(dice)

	def _nrolls(self, lhs, ops):
		"""
		Function for applying binary operations in which you roll self
		lhs times

		Parameters
		----------
		lhs: type(self)
			The unit which indicates how many of self we roll
		ops: Callable
			The operation between the unit.

		Returns
		-------
		out: type(self)
			The new unit representing the operation
		"""
		if isinstance(lhs, Number):
			return self._nrolls_lvl0(lhs, ops)
		elif issubclass(type(lhs), DieUnit):
			return self._nrolls_lvl1(lhs, ops)
		else:
			raise ValueError("Unexpected type in dice matmul")

	def __call__(self, mapping):
		"""
		Used to wrap the unit in as decorator. It used the map function.

		Parameters
		----------
		func:
			The function to wrap.

		Returns
		-------
		out: callable
			A function that returns a unit of the mapped function
		"""

		def wrapper():
			return self.map(mapping)

		return wrapper

	def __rmatmul__(self, lhs):
		"""
		Return lhs @ self
		"""
		return self._nrolls(lhs, ops.add)

	def __matmul__(self, rhs):
		"""
		Return self @ rhs
		"""
		return self._nrolls(rhs, ops.add)

	def __str__(self):
		res = (
			f"Die with mu - {self.mean:.2f}, sigma - {self.std:.2f},"
			f" faces - {len(self.outcomes)}\n"
		)  # noqa: E501h
		res += "-" * (len(res) - 1) + "\n"
		return res + str_plot(self, PLOT_WIDTH)

	def __hash__(self):
		return super().__hash__()

	@staticmethod
	def _expand(data):
		"""
		Function that expands dice into a sequence of numbers.

		Parameters
		----------
		data: dict
			Dict of numbers and dict which are then expanded.
			Eg. [1,2,3,d4] -> [1,2,3,4]

		Returns
		-------
		out: dict
			A dict with the expanded values and data.
		"""
		dice = defaultdict(
			int, filter(lambda x: issubclass(type(x[0]), DieUnit), data.items())
		)
		numbers = defaultdict(
			int, filter(lambda x: x[0] not in dice, data.items())
		)
		for i, die in enumerate(dice):
			for f in numbers.keys():
				numbers[f] *= die._units
			for d in dice:
				if d == die:
					continue
				dice[d] *= die._units
		for die, c in dice.items():
			for f, cd in die.items():
				numbers[f] += c * cd
		return numbers

	def sort(self):
		"""
		Function that sorts a the unit outcomes
		"""
		self.data = dict(sorted(self.items(), key=lambda pair: pair[0]))

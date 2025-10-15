import operator as ops
import warnings as wa
from collections import defaultdict
from numbers import Number

from dicechanics._strplot import str_plot
from dicechanics.baseunits.CombinationsUnit import MathOpsUnit

PLOT_WIDTH = 20


class DieUnit(MathOpsUnit):
	def __init__(self, data=None, /, **kwargs):
		super().__init__(self.expand(data), **kwargs)
		self.sort()

	f = MathOpsUnit.outcomes

	def reroll(self, redo, depth=1):
		if depth == "inf":
			return type(self)(
				{key: value for key, value in self if key not in redo}
			)
		faces = self._data
		for _ in range(depth):
			numbers = {f: c for f, c in faces.items() if f not in redo}
			dice = {self: sum(c for f, c in faces.items() if f in redo)}
			faces = self.expand(numbers | dice)
		return type(self)(faces)

	def _plode(self, ops, ploder, depth=1):
		if depth > 0:
			numbers = {f: c for f, c in self.items() if f not in ploder}
			dice = {
				(ops(f, self._plode(ops, *ploder, depth=depth - 1))): c
				for f, c in self.items()
				if f in ploder
			}
			faces = self.expand(numbers | dice)
		return type(self)(faces)

	def explode(self, exploder, depth=1):
		return self._plode(ops.add, *exploder, depth=depth)

	def implode(self, imploder, depth=1):
		return self._plode(ops.sub, *imploder, depth=depth)

	def count(self, targets):
		res = defaultdict(int)
		for key, val in self.items():
			res[key in self] += val
		return type(self)(res)

	def folding(self, rhs, ops, into):
		data = defaultdict(
			int, {f: c for f, c in self.items() if not ops(f, rhs)}
		)
		c = sum(c for f, c in self.items() if ops(f, rhs))
		data[into] += c
		return type(self)(data)

	def fold_over(self, rhs, /, into=None):
		return self.folding(rhs, ops.gt, into=rhs if into is None else into)

	def fold_under(self, rhs, /, into=None):
		return self.folding(rhs, ops.lt, into=rhs if into is None else into)

	def nrolls_lvl0(self, lhs, ops):
		if lhs == 0:
			wa.warn("A 0d have been rolled", RuntimeWarning)
			return type(self)({0: 1})
		if neg := lhs < 0:
			lhs *= -1
		res = self
		for _ in range(lhs - 1):
			res = ops(res, self)
		return -res if neg else res

	def nrolls_lvl1(self, lhs, ops):
		dice = defaultdict(int)
		for f, c in self.items():
			die = lhs.nrolls_lvl0(f, ops)
			dice[die] += c
		return type(self)(dice)

	def nrolls(self, lhs, ops):
		if isinstance(lhs, Number):
			return self.nrolls_lvl0(lhs, ops)
		elif issubclass(type(lhs), DieUnit):
			return self.nrolls_lvl1(lhs, ops)
		else:
			raise ValueError("Unexpected type in dice matmul")

	def __call__(self, mapping):
		def wrapper():
			return self.map(mapping)

		return wrapper

	def __rmatmul__(self, lhs):
		"""
		Return value @ self
		"""
		return self.nrolls(lhs, ops.add)

	def __matmul__(self, rhs):
		return self.nrolls(rhs, ops.add)

	def __str__(self):
		res = (
			f"Die with mu - {self.mean:.2f}, sigma - {self.std:.2f},"
			" faces - {len(self.outcomes)}\n"
		)  # noqa: E501h
		res += "-" * (len(res) - 1) + "\n"
		return res + str_plot(self, PLOT_WIDTH)

	def __repr__(self):
		return super().__repr__()

	def __hash__(self):
		return super().__hash__()

	@staticmethod
	def expand(data):
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
				if d != die:
					dice[d] *= die._units
		for die, c in dice.items():
			for f, cd in die.items():
				numbers[f] += c * cd
		return numbers

	def sort(self):
		"""
		Function that sorts a the die
		"""
		self.data = dict(sorted(self.items(), key=lambda pair: pair[0]))

__all__ = ["Die"]
from collections import defaultdict
from collections.abc import Callable
from numbers import Number

from ttstatistics.core.genericmapping import GenericMapping
from ttstatistics.core.group import Group
from ttstatistics.core.operations.macro import Operators
from ttstatistics.core.operations.micro import add, div, floorDiv, mul, sub
from ttstatistics.core.protocols.base import InputFunction, Unit
from ttstatistics.core.protocols.mapping import Mapping
from ttstatistics.dicechanics import protocols
from ttstatistics.dicechanics.protocols import Statistical
from ttstatistics.dicechanics.statisticals.scalar import ScalarStatistical
from ttstatistics.dicechanics.symbolics import RerollSymbol
from ttstatistics.utils._plot import StringPlot

type MapFunction = Callable[[Unit], Unit]


class Die(GenericMapping, protocols.Die):
	def __init__(self, data: Statistical[Unit] = ScalarStatistical()):
		inpt = type(data)(self._expand(data))
		super().__init__(inpt)

	def __bool__(self):
		return False

	@property
	def mean(self):
		return self.internals.mean

	@property
	def varians(self):
		return self.internals.varians

	@property
	def std(self):
		return self.internals.std

	def map(self, mapping: MapFunction) -> protocols.Die:
		return type(self)(self.internals.map(mapping))

	def _binaryOperaiton(self, rhs, operation: InputFunction):
		if isinstance(rhs, Number):
			internal = defaultdict(lambda: 0)
			for key, prob in self.items():
				internal[operation(key, rhs)] += prob
			return type(self)(type(self.internals)(internal))
		else:
			if rhs == self:
				group = Group({self: 2})
			else:
				group = Group({self: 1, rhs: 1})
			newMapping = type(self.internals)(
				Operators.regularOnGroup(group, operation)
			)
			return type(self)(newMapping)

	def __add__(self, rhs):
		return self._binaryOperaiton(rhs, add)

	def __radd__(self, rhs):
		return self.__add__(rhs)

	def __sub__(self, rhs):
		return self._binaryOperaiton(rhs, sub)

	def __rsub__(self, rhs):
		return (-self).__add__(rhs)

	def __mul__(self, rhs):
		return self._binaryOperaiton(rhs, mul)

	def __rmul__(self, rhs):
		return self._binaryOperaiton(rhs, mul)

	def __floordiv__(self, rhs):
		return self._binaryOperaiton(rhs, floorDiv)

	def __truediv__(self, rhs):
		return self._binaryOperaiton(rhs, div)

	def _expand(self, statistical: Statistical):
		dice = list(
			filter(
				lambda x: isinstance(x[0], (Mapping, RerollSymbol)),
				statistical.items(),
			)
		)
		numbers = defaultdict(
			lambda: 0,
			filter(
				lambda x: not isinstance(x[0], (Mapping)), statistical.items()
			),
		)
		for die, dieProb in dice:
			if isinstance(die, RerollSymbol):
				mapping = self
			else:
				mapping = die
			for face, prob in mapping.items():
				numbers[face] += prob * dieProb
		return type(statistical)(numbers)

	def count(self, *facesToCount):
		return self.map(lambda key: key in facesToCount)

	def _rerollBaseline(
		self, rerollMapping: Mapping, *faceToReroll, depth, ops
	):
		newMap = self
		for _ in range(depth):
			tokeep = dict(
				filter(lambda x: x[0] not in faceToReroll, self.items())
			)
			for face in faceToReroll:
				rerollSum = sum(
					dict(filter(lambda x: x[0] == face, self.items())).values()
				)
				map_ = ops(face, newMap)
				if map_ in tokeep:
					tokeep[map_] += rerollSum
				else:
					tokeep.update({ops(face, newMap): rerollSum})
			newMap = type(self.internals)(self._expand(tokeep))
		return newMap

	def reroll(self, *faceToReroll, depth=1):
		rerolledMapping = self._rerollBaseline(
			self, *faceToReroll, depth=depth, ops=lambda x, y: y
		)
		return type(self)(type(self.internals)(rerolledMapping))

	def explode(self, *faceToReroll, depth=1):
		rerolledMapping = self._rerollBaseline(
			self, *faceToReroll, depth=depth, ops=add
		)
		return type(self)(type(self.internals)(rerolledMapping))

	def implode(self, *faceToReroll, depth=1):
		rerolledMapping = self._rerollBaseline(
			self, *faceToReroll, depth=depth, ops=sub
		)
		return type(self)(type(self.internals)(rerolledMapping))

	def __str__(self):
		res = f"Die with mu - {self.mean:.2f}, sigma - {self.std:.2f}\n"
		res += "-" * (len(res) - 1) + "\n"
		return res + StringPlot.bars(
			self.keys(),
			self.values(),
			topText=[f"{i * 100:.2f}%" for i in self.values()],
		)

	def __neg__(self):
		return self.map(lambda x: -x)

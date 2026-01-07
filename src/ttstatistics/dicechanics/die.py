__all__ = ["Die"]
from collections import defaultdict
from collections.abc import Callable
from numbers import Number

from ttstatistics.core.group import Group
from ttstatistics.core.mapping import GenericMapping, expand
from ttstatistics.core.operations import (
	add,
	div,
	floorDiv,
	ge,
	gt,
	le,
	lt,
	mul,
	perform,
	sub,
)
from ttstatistics.core.protocols.base import InputFunction, Unit
from ttstatistics.core.protocols.mapping import Mapping
from ttstatistics.dicechanics import protocols
from ttstatistics.dicechanics.pool import Pool
from ttstatistics.dicechanics.protocols import Statistical
from ttstatistics.dicechanics.statisticals.factory import createStatistical
from ttstatistics.dicechanics.statisticals.scalar import ScalarStatistical
from ttstatistics.utils._plot import StringPlot
from ttstatistics.utils.utils import sort_dict

type MapFunction = Callable[[Unit], Unit]


class Die(GenericMapping, protocols.Die):
	def __init__(self, data: Statistical[Unit] = ScalarStatistical()):
		inpt = createStatistical(expand(data))
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
		res = defaultdict(lambda: 0)
		for key, value in self.items():
			res[mapping(key)] += value
		return type(self)(createStatistical(res))

	def _binaryOperaiton(self, rhs, operation: InputFunction):
		if isinstance(rhs, Number):
			rhs = type(self)(createStatistical({rhs: 1}))
		if rhs == self:
			group = Group({self: 2})
		else:
			group = Group({self: 1, rhs: 1})
		statistical = createStatistical(perform(group, operation))
		return type(self)(statistical)

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

	def __gt__(self, rhs):
		return self._binaryOperaiton(rhs, gt)

	def __ge__(self, rhs):
		return self._binaryOperaiton(rhs, ge)

	def __lt__(self, rhs):
		return self._binaryOperaiton(rhs, lt)

	def __le__(self, rhs):
		return self._binaryOperaiton(rhs, le)

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
			newMap = type(self)(createStatistical(tokeep))
		return newMap

	def reroll(self, *faceToReroll, depth=1) -> protocols.Die:
		rerolledMapping = self._rerollBaseline(
			self, *faceToReroll, depth=depth, ops=lambda _, y: y
		)
		return type(self)(rerolledMapping)

	def explode(self, *faceToReroll, depth=1) -> protocols.Die:
		rerolledMapping = self._rerollBaseline(
			self, *faceToReroll, depth=depth, ops=add
		)
		return type(self)(rerolledMapping)

	def implode(self, *faceToReroll, depth=1) -> protocols.Die:
		rerolledMapping = self._rerollBaseline(
			self, *faceToReroll, depth=depth, ops=sub
		)
		return type(self)(rerolledMapping)

	def __str__(self):
		res = "Die with mu - "
		res += f"{self.mean:.2f}" if self.mean is not None else "n/a"
		res += ", sigma - "
		res += f"{self.std:.2f}" if self.std is not None else "n/a"
		res += "\n"
		res += "-" * (len(res) - 1) + "\n"
		data = sort_dict(self)
		return res + StringPlot.bars(
			data.keys(),
			data.values(),
			topText=[f"{i * 100:.2f}%" for i in data.values()],
		)

	def __neg__(self):
		return self.map(lambda x: -x)

	@property
	def dtype(self) -> Statistical:
		return type(self.internals)

	def __matmul__(self, rhs: int) -> protocols.Pool:
		if isinstance(rhs, Die):
			pass
		elif isinstance(rhs, int):
			return Pool({self: rhs})
		else:
			raise TypeError

	def __rmatmul__(self, rhs: int) -> protocols.Pool:
		return self @ rhs

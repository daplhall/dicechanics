import math
from collections import defaultdict
from collections.abc import MutableMapping
from numbers import Number

from dicechanics.utils import sort_dict


class StatisticalUnit[T](MutableMapping[T, int]):
	"""test"""

	def __init__(self, data=None, /, **kwargs):
		self.data = data
		self._derived_attr()

	def _derived_attr(self):
		self.isnum = all(isinstance(i, Number) for i in self.keys())
		self._units = sum(self.values())

	def copy(self):
		"""
		Function that creates a copy of the unit

		Returns
		-------
		out: type(self)
			The copy
		"""
		return type(self)(self)

	def map(self, mapping):
		"""
		Maps a function onto the die

		Parameters
		----------
		func: Callable
			The function to be mapped

		Returns
		-------
		out: type(self)
			The die with the results of the mapping
		"""
		res = defaultdict(int)
		for key, value in self.items():
			res[mapping(key)] += value
		return type(self)(res)

	def simplify(self):
		"""
		Function that simplifies the counts of the unit outcomes.
		"""
		r = None
		neigh = iter(self.values())
		next(neigh)
		for a, b in zip(super().values(), neigh):
			if r is not None:
				r = self._gcd(r, b)
			else:
				r = self._gcd(a, b)
			if r == 1:
				break
		if len(self) > 1:
			self.data.update({key: count // r for key, count in self.items()})
			self._derived_attr()

	@staticmethod
	def _gcd(a, b):
		while b != 0:
			a, b = b, a % b
		return a

	@property
	def probability(self):
		"""
		Returns the probability for the outcomes

		Returns
		-------
		out: List
			The probability of the outcomes.
		"""
		return [i / self._units for i in sort_dict(self).values()]

	p = probability

	@property
	def counts(self):
		"""
		Returns the count list of the unit.

		Returns
		-------
		out: list
			The number pr face of the unit.
		"""
		return list(sort_dict(self.data).values())

	c = counts

	@property
	def outcomes(self):
		"""
		Returns the outcomes of the unit

		Returns
		-------
		out: list
			The outcomes of the unit.
		"""
		return list(sort_dict(self.data).keys())

	o = outcomes

	@property
	def mean(self):
		"""
		Returns the mean of the unit

		Returns
		-------
		out: Number
			The mean of the unit.
		"""
		if not self.isnum:
			return None
		return sum(p * f for p, f in zip(self.probability, self.outcomes))

	@property
	def variance(self):
		"""
		Returns the variance of the unit

		Returns
		-------
		out: Number
			The variance of the unit.
		"""
		if not self.isnum:
			return None
		return sum(
			p * (x - self.mean) ** 2
			for x, p in zip(self.outcomes, self.probability)
		)

	@property
	def std(self):
		"""
		Returns the standard deviation of the unit

		Returns
		-------
		out: Number
			The standard deviations of the unit.
		"""
		if not self.isnum:
			return None
		return math.sqrt(self.variance)

	@property
	def cdf(self):
		"""
		Returns the cumulative probability of the die

		Returns
		-------
		out: List
			The cumulative probability for the outcomes.
		"""
		if not self.isnum:
			return None
		cdf = []
		for p in self.probability:
			cdf.append(p + cdf[-1] if cdf else p)
		return cdf

	@property
	def min(self):
		"""
		Returns the minimum faces of the unit

		Parameters
		-------
		out: Number | None
			The minimum face of the unit
		"""
		return min(self.outcomes) if self.isnum else None

	@property
	def max(self):
		"""
		Returns the maximum face of the unit.

		Parameters
		-------
		out: float
			The maximum face of the unit.
		"""
		return max(self.outcomes) if self.isnum else None

	def __hash__(self):
		return hash(tuple(self.outcomes) + tuple(self.counts) + (self.mean,))

	def __setitem__(self, key, item):
		"""
		Sets the item located at key.

		functions like a dict[key] = value
		"""
		retrn = self.data[key] = item
		self._derived_attr()
		return retrn

	def __getitem__(self, key):
		return self.data[key]

	def __delitem__(self, key):
		del self.data[key]
		self._derived_attr()

	def __iter__(self):
		return iter(self.data)

	def __len__(self):
		return len(self.data)

	def __repr__(self):
		return (
			f"{type(self).__name__}"
			"({"
			f"{', '.join('{}: {}'.format(*i) for i in self.items())}"
			"})"
		)

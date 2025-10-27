import math
from collections import defaultdict
from numbers import Number

from dicechanics._inpt_cleaning import sort_dict


class StatisticalUnit(dict):
	"""test"""

	def __init__(self, data=None, /, **kwargs):
		super().__init__(data, **kwargs)
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
			self.update({key: count // r for key, count in self.items()})

	def __repr__(self):
		return f"{type(self).__name__}({super().__repr__()})"

	def clear(self):
		"""
		clears the unit.

		functions like dict.clear()
		"""
		super().clear()
		self._derived_attr()

	def pop(self, index=-1, /):
		"""
		pops the value for the given index

		Functions like a dict.pop
		"""
		retrn = super().pop(index)
		self._derived_attr()
		return retrn

	def popitem(self):
		"""
		pops the set of (key, item)

		Functions like a dict.popitem
		"""
		retrn = super().popitem()
		self._derived_attr()
		return retrn

	def extend(self, iterable, /):
		"""
		Extends the underlying dict.

		functions like dict.extend
		"""
		super().extend(iterable)
		self._derived_attr()

	def update(self, other=None, **kwargs):
		"""
		updates the underlying dict.

		functions like dict.update
		"""
		super().update(other, **kwargs)
		self._derived_attr()

	def items(self):
		"""
		returns an iterator for (keys, items) for the underlying dict.

		functions like dict.items()
		"""
		return super().items()

	def keys(self):
		"""
		returns an iterator for (key) for the underlying dict.

		functions like dict.items()
		"""
		return super().keys()

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
		return list(sort_dict(super()).values())

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
		return list(sort_dict(super()).keys())

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
		retrn = super().__setitem__(key, item)
		self._derived_attr()
		return retrn

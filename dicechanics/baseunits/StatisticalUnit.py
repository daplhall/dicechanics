import math
from collections import UserDict, defaultdict
from numbers import Number


class StatisticalUnit(UserDict):
	def __init__(self, data=None, /, **kwargs):
		super().__init__(data, **kwargs)
		self.isnum = all(isinstance(i, Number) for i in super().keys())

		self._units = sum(super().values())
		self._p = [i / self._units for i in super().values()]

		self._mean = (
			self.calc_mean(self.p, self.outcomes) if self.isnum else None
		)
		self._var = (
			self.calc_varians(self.p, self.outcomes, self.mean)
			if self.isnum
			else None
		)
		self._std = math.sqrt(self._var) if self.isnum else None
		self._cdf = self.calc_cumulative(self.p)

	def __hash__(self):
		return hash(tuple(self.items()) + (self.mean,))

	def copy(self):
		return type(self)(self)

	def map(self, mapping):
		res = defaultdict(int)
		for key, value in self.items():
			res[mapping(key)] += value
		return type(self)(res)

	@staticmethod
	def calc_mean(probability, outcomes):
		return sum(p * f for p, f in zip(probability, outcomes))

	@staticmethod
	def calc_varians(probability, outcomes, mean):
		return sum(p * (x - mean) ** 2 for x, p in zip(outcomes, probability))

	@staticmethod
	def calc_cumulative(properbility):
		cdf = []
		for p in properbility:
			cdf.append(p + cdf[-1] if cdf else p)
		return cdf

	@staticmethod
	def gcd(a, b):
		while b != 0:
			a, b = b, a % b
		return a

	@property
	def probability(self):
		return self._p

	p = probability

	@property
	def cdf(self):
		return self._cdf

	@property
	def counts(self):
		return list(super().values())

	c = counts

	@property
	def outcomes(self):
		return list(super().keys())

	o = outcomes

	@property
	def mean(self):
		return self._mean

	@property
	def varians(self):
		return self._var

	@property
	def std(self):
		return self._std

	@property
	def min(self):
		return min(self.outcomes) if self.isnum else None

	@property
	def max(self):
		return max(self.outcomes) if self.isnum else None

	def simplify(self):
		r = None
		neigh = iter(super().values())
		next(neigh)
		for a, b in zip(super().values(), neigh):
			if r is not None:
				r = self.gcd(r, b)
			else:
				r = self.gcd(a, b)
			if r == 1:
				break
		if len(self) > 1:
			for key, count in super().items():
				super().__setitem__(key, count // r)

	def __repr__(self):
		return f"{type(self).__name__}({self.data})"

from typing import Iterable


def unique(array: Iterable[float]) -> tuple[list, list]:
	"""
	Function that finds the unique values in an iterable and their occurences.

	Paramters
	---------
	array: Iterable
		The array of objects which one wants to find the unique values of.

	Returns
	-------
	uniques: list
		The unique values.
	count: list
		The occurences of the unique values.
	"""
	uf = []
	c = []
	for e in array:
		if e not in uf:
			uf.append(e)
			c.append(1)
		else:
			i = uf.index(e)
			c[i] += 1
	return uf, c


def gcd(a: int, b: int) -> int:
	"""
	Find the greatest commen demoninator between a and b

	Parameters
	----------
	a: int
	b: int

	Returns
	-------
	out: int
		Greatest common demominator
	"""
	while b != 0:
		r = a % b
		a, b = b, r
	return a

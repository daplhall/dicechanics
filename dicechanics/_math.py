from typing import Iterable


def unique(array: Iterable[float]) -> tuple[list, list]:
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
	Greatest commen demoninator
	"""
	while b != 0:
		r = a % b
		a, b = b, r
	return a

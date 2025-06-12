__all__ = ['add', 'sub', 'mul', 'floordiv', 'div','mod','ceil','floor']
import math
import operator as op
from typing import Iterable

add = op.add
sub = op.sub
mul = op.mul
floordiv = op.floordiv
div = op.truediv
mod = op.mod
ceil = math.ceil
floor = math.floor
max = max
min = min

def unique(array: Iterable[float]) -> tuple[list,list]:
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

def ceildiv(lhs: float, rhs: float) -> float:
	return -(lhs//-rhs)

def gcd(a: int, b: int) -> int:
	"""
	Greatest commen demoninator
	"""
	while b != 0:
		r = a%b
		a,b = b, r
	return a
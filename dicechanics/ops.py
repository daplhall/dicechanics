__all__ = ['add', 'sub', 'mul', 'floordiv', 'div','mod','ceil','floor']

import math
import operator as op

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

def ceildiv(lhs: float, rhs: float) -> float:
	return -(lhs//-rhs)
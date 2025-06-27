"""
Module that contains some simple linear operations to use with :py:class:`dicechanics.Pool`
"""  # noqa: E501

__all__ = ["add", "sub", "mul", "floordiv", "div", "mod", "ceil", "floor"]

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


def ceildiv(numer: float, denom: float) -> float:
	"""
	Division that rounds up instead of down.

	Parameters
	----------
	numer: float
		The numerator of the division
	denom: float
		The denominator of the division

	"""
	return -(numer // -denom)

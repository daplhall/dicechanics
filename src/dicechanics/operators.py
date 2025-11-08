"""
Module that contains some simple linear operations to use with :py:class:`dicechanics.Pool`
"""  # noqa: E501

__all__ = ["add", "sub", "mul", "floorDiv", "div", "mod", "ceil", "floor"]

import math
import operator as op

add = op.add
sub = op.sub
mul = op.mul
floorDiv = op.floordiv
div = op.truediv
mod = op.mod
ceil = math.ceil
floor = math.floor
max = max
min = min

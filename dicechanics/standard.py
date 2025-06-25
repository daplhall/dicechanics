"""
Module that defines the standard dice that you can by in a store
Hello
"""

__all__ = ["d4", "d6", "d8", "d10", "d12", "d20", "d100", "z9"]

from dicechanics._interface import d, z

d4 = d(4)
d6 = d(6)
d8 = d(8)
d10 = d(10)
d12 = d(12)
d20 = d(20)
d100 = d(100)
z9 = z(9)

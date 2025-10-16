__all__ = ["d", "pool", "z"]

from collections.abc import Iterable

from dicechanics._parser import text_to_faces
from dicechanics.Die import Die
from dicechanics.Pool import Pool


def d(inpt: Iterable | int | Die | dict, **kwards) -> Die:
	"""
	Function that creates a die from various input types
	Currently takes int, str, Iterable, Die which it copies, and a dict

	Parameters
	----------
	inpt: Iterable | Int | Die | dict
		the input for the function
	**kwards
		Rounding: Callable

	Returns
	-------
	out: Die
		The die created from the input
	"""
	if isinstance(inpt, int):
		return Die(dict.fromkeys(range(1, inpt + 1), 1), **kwards)
	elif isinstance(inpt, str):
		faces = text_to_faces(inpt)
		return Die(faces, **kwards)
	elif isinstance(inpt, Die):
		return inpt.copy()
	elif isinstance(inpt, dict):
		return Die(inpt)
	elif isinstance(inpt, Iterable):
		return Die(dict.fromkeys(inpt, 1), **kwards)
	else:
		raise Exception(f"Dice doesn't support input type of {type(inpt)}")


def z(inpt: int, **kwards) -> Die:
	"""
	Function that creates a z-die from various input types

	A z-die is a die which starts from 0. So a z9 is a die going from [0..9]

	Parameters
	----------
	inpt: int
		the input for the function

	Returns
	-------
	out: Die
		The die created from the input
	"""
	return Die(dict.fromkeys(range(0, inpt + 1), 1), **kwards)


def pool(inpt: list) -> Pool:
	"""
	Creates a pool from a list of number and/or dice.

	Parameters
	----------
	inpt: list
		list of numbers or dice

	Returns
	-------
	out: Pool
		The pool containing the elements of the input
	"""
	return Pool(inpt)

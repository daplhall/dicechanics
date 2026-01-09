from collections import defaultdict
from collections.abc import Iterable
from numbers import Number

from ttstatistics.core.protocols.mapping import Mapping
from ttstatistics.dicechanics import protocols
from ttstatistics.dicechanics.die import Die
from ttstatistics.dicechanics.parser import ParserMetaData, parser
from ttstatistics.dicechanics.pool import Pool
from ttstatistics.dicechanics.statisticals import (
	ScalarStatistical,
	StringStatistical,
)
from ttstatistics.utils.utils import normalize, unique


def _convertToCorrectStatistical(obj):
	if all(isinstance(key, Number) for key in obj.keys()):
		backend = ScalarStatistical(obj)
	elif all(isinstance(key, str) for key in obj.keys()):
		backend = StringStatistical(obj)
	else:
		raise TypeError("Mapping keys are not of a supported type")
	return Die(backend)


def d(obj: int | Iterable | str) -> protocols.Die:
	"""
	The default way of creating a Die

	Parameters
	----------
	obj: int | Iterable | str
		A python obj that is that is taken an transformed into a Die.\n
		1. When an Int it defines the die through dice syntax eg. d(42) is a  d42.\n
		2. When an iterable it counts the repeated faces eg. d([1,1,1,3]) becomes a die with 3 sides as 1.\n
		3. When a string it follows a specific syntax "<start>..<end>:<repeat>, <new statement>"\n
	Returns
	-------
	out: Die
		The dice representing the input
	"""  # noqa: E501
	if isinstance(obj, int):
		backend = ScalarStatistical(dict.fromkeys(range(1, obj + 1), 1 / obj))
		return Die(backend)
	elif isinstance(obj, str):
		res = defaultdict(lambda: 0)
		for segment in obj.split(","):
			meta = ParserMetaData(segment)
			occurences = parser.run(meta)
			for key, count in occurences.output.items():
				res[key] += count
		normalizedOutput = normalize(res)
		return _convertToCorrectStatistical(normalizedOutput)
	elif isinstance(obj, Iterable):
		uniques = unique(obj)
		norm = sum(uniques.values())
		return _convertToCorrectStatistical(
			{key: count / norm for key, count in uniques.items()}
		)
	else:
		raise TypeError("Unsupported type")


def pool(input: dict[protocols.Die, int | protocols.Die]):
	"""
	The default function for creating a pool. Matmult on dice is recommended over this.

	Parameters
	----------
	input:  dict[Die]
		A dict of dice. The values are the amount of said die in the pool.
	Returns
		out: Pool
	"""  # noqa: E501
	return Pool(input)

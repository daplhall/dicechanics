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


def d(obj: int | Iterable | Mapping) -> protocols.Die:
	if isinstance(obj, int):
		backend = ScalarStatistical(dict.fromkeys(range(1, obj + 1), 1 / obj))
		return Die(backend)
	elif isinstance(obj, Mapping):
		return _convertToCorrectStatistical(obj)
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


def pool(input: dict[protocols.Die, int]):
	return Pool(input)

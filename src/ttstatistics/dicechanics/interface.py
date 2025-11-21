from collections.abc import Iterable
from numbers import Number

from ttstatistics.core.protocols.mapping import Mapping
from ttstatistics.dicechanics.die import Die
from ttstatistics.dicechanics.statisticals import (
	ScalarStatistical,
	StringStatistical,
)
from ttstatistics.utils.utils import unique


def _convertToCorrectStatistical(obj):
	if all(isinstance(key, Number) for key in obj.keys()):
		backend = ScalarStatistical(obj)
	elif all(isinstance(key, str) for key in obj.keys()):
		backend = StringStatistical(obj)
	else:
		raise TypeError("Mapping keys are not of a supported type")
	return Die(backend)


def d(obj: int | Iterable | Mapping):
	if isinstance(obj, int):
		backend = ScalarStatistical(dict.fromkeys(range(1, obj + 1), 1 / 6))
		return Die(backend)
	elif isinstance(obj, Mapping):
		return _convertToCorrectStatistical(obj)
	elif isinstance(obj, str):
		return None
	elif isinstance(obj, Iterable):
		uniques = unique(obj)
		norm = sum(uniques.values())
		return _convertToCorrectStatistical(
			{key: count / norm for key, count in uniques.items()}
		)
	else:
		raise TypeError("Unsupported type")

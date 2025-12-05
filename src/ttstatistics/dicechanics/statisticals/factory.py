from enum import IntEnum, auto
from numbers import Number
from typing import Any

from ttstatistics.core.protocols import Mapping
from ttstatistics.dicechanics import protocols
from ttstatistics.dicechanics.statisticals import (
	BaseStatistical,
	ScalarStatistical,
	StringStatistical,
)


class ScalarFactory(protocols.StatisticalFactory):
	def create(self, data: Mapping[Number, Number]):
		return ScalarStatistical(data)


class GenericFactory(protocols.StatisticalFactory):
	def create(self, data: Mapping[Any, Number]):
		return BaseStatistical(data)


class StringFactory(protocols.StatisticalFactory):
	def create(self, data: Mapping[str, Number]):
		return StringStatistical(data)


class FactoryEnum(IntEnum):
	MIXED = auto()
	EMPTY = auto()


def _isMixed(typing):
	return typing == FactoryEnum.MIXED


def _isNumber(typing):
	return issubclass(typing, Number)


def _isBothNumbers(typing, otherType):
	return _isNumber(typing) and _isNumber(otherType)


def _isString(typing):
	return issubclass(typing, str)


def _isSameType(typing, otherType):
	return issubclass(typing, otherType)


def _isEmpty(typing):
	return typing == FactoryEnum.EMPTY


def _whichDataType(data: Mapping[Any, Number]) -> type | FactoryEnum:
	if not data:
		return FactoryEnum.EMPTY
	keys = iter(data.keys())
	typing = type(next(keys))
	for key in keys:
		if not _isBothNumbers(typing, type(key)) and not _isSameType(
			typing, type(key)
		):
			typing = FactoryEnum.MIXED
			break
	return typing


def _whichFactory(data: Mapping[Any, Number]) -> protocols.StatisticalFactory:
	typing = _whichDataType(data)
	if _isEmpty(typing) or _isMixed(typing):
		return GenericFactory
	elif _isNumber(typing):
		return ScalarFactory
	elif _isString(typing):
		return StringFactory
	else:
		raise Exception("You shouldn't be here; Statistical creation")


def createStatistical(
	data: Mapping[Any, Number],
) -> protocols.StatisticalFactory:
	return _whichFactory(data)().create(data)

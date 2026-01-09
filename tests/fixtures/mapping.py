import pytest

from ttstatistics.core import protocols
from ttstatistics.core.mapping import GenericMapping


class MappingMock(protocols.Mapping):
	def __init__(self, data={}):
		self.data = data

	def items(self):
		return self.data.items()

	def keys(self):
		return self.data.keys()

	def values(self):
		return self.data.values()


@pytest.fixture
def emptyDict():
	return MappingMock()


@pytest.fixture
def simpleScalarMock(referenceStatisticalDict):
	return MappingMock(referenceStatisticalDict)


@pytest.fixture
def AltScalarMock(alternativeReferenceDict):
	return MappingMock(alternativeReferenceDict)


@pytest.fixture
def FlatMapping3():
	return GenericMapping(dict.fromkeys(range(1, 4), 1 / 3))


@pytest.fixture
def FlatMappingOdd3Values():
	return GenericMapping({1: 1 / 3, 3: 1 / 3, 5: 1 / 3})


@pytest.fixture
def FlatMapping4():
	return GenericMapping(dict.fromkeys(range(1, 5), 1 / 4))


@pytest.fixture
def FlatMapping6():
	return GenericMapping(dict.fromkeys(range(1, 7), 1 / 6))

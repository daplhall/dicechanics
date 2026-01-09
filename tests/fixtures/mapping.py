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
def FlatMapping3():
	return GenericMapping({1: 1 / 3, 2: 1 / 3, 3: 1 / 3})


@pytest.fixture
def FlatMapping4():
	return GenericMapping({1: 1 / 4, 2: 1 / 4, 3: 1 / 4, 4: 1 / 4})

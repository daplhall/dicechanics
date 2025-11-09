import pytest

from ttstatistics.core import protocols


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

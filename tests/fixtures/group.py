import pytest

from fixtures.mapping import MappingMock
from ttstatistics.core.group import Group


@pytest.fixture
def GroupEmpty():
	return Group()


@pytest.fixture
def Group2Dublicate(simpleScalarMock):
	return Group({simpleScalarMock: 2})


@pytest.fixture
def Group2Items(simpleScalarMock, AltScalarMock):
	return Group({simpleScalarMock: 1, AltScalarMock: 1})


@pytest.fixture
def Group4Items(alternativeReferenceDict):
	a = MappingMock(alternativeReferenceDict)
	b = MappingMock(alternativeReferenceDict)
	c = MappingMock(alternativeReferenceDict)

	return Group(
		{
			a: 2,
			b: 1,
			c: 1,
		}
	)


@pytest.fixture
def Group3Flat6(FlatMapping6):
	return Group({FlatMapping6: 3})


@pytest.fixture
def GroupMixed(FlatMapping3, FlatMapping4):
	return Group({FlatMapping3: 3, FlatMapping4: 2})


@pytest.fixture
def GroupOddValues3(FlatMappingOdd3Values):
	return Group({FlatMappingOdd3Values: 3})

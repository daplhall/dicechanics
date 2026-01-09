import pytest

from fixtures.mapping import MappingMock
from ttstatistics.core.group import Group


@pytest.fixture
def GroupEmpty():
	return Group()


@pytest.fixture
def groupWithItems(simpleScalarMock):
	return Group({simpleScalarMock: 2})


@pytest.fixture
def groupWithTwoItems(simpleScalarMock, alternativeReferenceDict):
	secondSimpleScalarMock = MappingMock(alternativeReferenceDict)

	return Group({simpleScalarMock: 1, secondSimpleScalarMock: 1})


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

import pytest

from fixtures.mapping import MappingMock
from ttstatistics.core.group import Group


@pytest.fixture
def emptyGroup():
	return Group()


@pytest.fixture
def groupWithItems(simpleScalarMock):
	return Group({simpleScalarMock: 2})


@pytest.fixture
def groupWithTwoItems(simpleScalarMock, alternativeReferenceDict):
	secondSimpleScalarMock = MappingMock(alternativeReferenceDict)

	return Group({simpleScalarMock: 1, secondSimpleScalarMock: 1})


@pytest.fixture
def groupWithFourItems(alternativeReferenceDict):
	firstSimpleScalarDie = MappingMock(alternativeReferenceDict)
	secondSimpleScalarDie = MappingMock(alternativeReferenceDict)
	thridSimpleScalarDie = MappingMock(alternativeReferenceDict)

	return Group(
		{
			firstSimpleScalarDie: 2,
			secondSimpleScalarDie: 1,
			thridSimpleScalarDie: 1,
		}
	)

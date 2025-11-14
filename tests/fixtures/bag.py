import pytest

from fixtures.mapping import MappingMock
from ttstatistics.core.group import Group


@pytest.fixture
def emptyBag():
	return Group()


@pytest.fixture
def bagWithItems(simpleScalarMock):
	return Group({simpleScalarMock: 2})


@pytest.fixture
def bagWithTwoItems(simpleScalarMock, alternativeReferenceDict):
	secondSimpleScalarMock = MappingMock(alternativeReferenceDict)

	return Group({simpleScalarMock: 1, secondSimpleScalarMock: 1})


@pytest.fixture
def bagWithFourItems(alternativeReferenceDict):
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

import pytest

from fixtures.mapping import MappingMock
from ttstatistics.core.bag import Bag


@pytest.fixture
def emptyBag():
	return Bag()


@pytest.fixture
def bagWithItems(simpleScalarMock):
	return Bag({simpleScalarMock: 2})


@pytest.fixture
def bagWithTwoItems(simpleScalarMock, alternativeReferenceDict):
	secondSimpleScalarMock = MappingMock(alternativeReferenceDict)

	return Bag({simpleScalarMock: 1, secondSimpleScalarMock: 1})


@pytest.fixture
def bagWithFourItems(alternativeReferenceDict):
	firstSimpleScalarDie = MappingMock(alternativeReferenceDict)
	secondSimpleScalarDie = MappingMock(alternativeReferenceDict)
	thridSimpleScalarDie = MappingMock(alternativeReferenceDict)

	return Bag(
		{
			firstSimpleScalarDie: 2,
			secondSimpleScalarDie: 1,
			thridSimpleScalarDie: 1,
		}
	)

import pytest

from dicechanics.bag import Bag
from dicechanics.die import Die


@pytest.fixture
def emptyBag():
	return Bag()


@pytest.fixture
def bagWithItems(simpleScalarDie):
	return Bag({simpleScalarDie: 2})


@pytest.fixture
def bagWithTwoItems(simpleScalarDie, alternativeReferenceDict):
	secondSimpleScalarDie = Die(alternativeReferenceDict)

	return Bag({simpleScalarDie: 1, secondSimpleScalarDie: 1})


@pytest.fixture
def bagWithFourItems(simpleScalarDie, alternativeReferenceDict):
	firstSimpleScalarDie = Die(alternativeReferenceDict)
	secondSimpleScalarDie = Die(alternativeReferenceDict)
	thridSimpleScalarDie = Die(alternativeReferenceDict)

	return Bag(
		{
			firstSimpleScalarDie: 2,
			secondSimpleScalarDie: 1,
			thridSimpleScalarDie: 1,
		}
	)

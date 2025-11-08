import pytest

from dicechanics.bag import Bag


@pytest.fixture
def emptyBag():
	return Bag()


@pytest.fixture
def bagWithItems(simpleScalarDie):
	return Bag({simpleScalarDie: 2})

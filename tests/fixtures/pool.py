import pytest

from dicechanics.pool import Pool


@pytest.fixture
def emptyPool():
	return Pool()


@pytest.fixture
def poolTwoLength(emptyDie):
	return Pool.from_list([emptyDie, emptyDie])


@pytest.fixture
def poolOneLength(emptyDie):
	return Pool.from_list([emptyDie])

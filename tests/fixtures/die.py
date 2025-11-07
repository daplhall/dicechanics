import pytest

from dicechanics.die import Die


@pytest.fixture
def emptyDie():
	return Die()

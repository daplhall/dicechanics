import pytest

from ttstatistics.dicechanics.die import Die
from ttstatistics.dicechanics.statisticals import ScalarStatistical


@pytest.fixture
def emptyDie():
	return Die()


@pytest.fixture
def simpleScalarDie(simpleScalarStatistical):
	return Die(simpleScalarStatistical)


@pytest.fixture
def simpleStringDie(simpleStringStatistical):
	return Die(simpleStringStatistical)


@pytest.fixture
def d4():
	return Die(ScalarStatistical({1: 1 / 4, 2: 1 / 4, 3: 1 / 4, 4: 1 / 4}))

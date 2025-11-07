import pytest

from dicechanics.die import Die


@pytest.fixture
def emptyDie():
	return Die()


@pytest.fixture
def simpleScalarDie(simpleScalarStatistical):
	return Die(simpleScalarStatistical)


@pytest.fixture
def simpleStringDie(simpleStringStatistical):
	return Die(simpleStringStatistical)

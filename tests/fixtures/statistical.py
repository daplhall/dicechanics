import pytest

from ttstatistics.dicechanics.statisticals.scalar import ScalarStatistical
from ttstatistics.dicechanics.statisticals.string import StringStatistical


@pytest.fixture
def emptyScalarStatistical():
	return ScalarStatistical()


@pytest.fixture
def referenceStatisticalDict():
	return {1: 1 / 4, 2: 2 / 4, 3: 1 / 4}


@pytest.fixture
def shiftedReferenceStatisticalDict():
	return {2: 1 / 4, 3: 2 / 4, 4: 1 / 4}


@pytest.fixture
def referenceStringDict():
	return {"a": 1 / 4, "b": 2 / 4, "c": 1 / 4}


@pytest.fixture
def downShiftedReferenceDict():
	return {0: 1 / 4, 1: 2 / 4, 2: 1 / 4}


@pytest.fixture
def alternativeReferenceDict():
	return {1: 2 / 5, 2: 2 / 5, 3: 1 / 5}


@pytest.fixture
def simpleScalarStatistical(referenceStatisticalDict):
	return ScalarStatistical(referenceStatisticalDict)


@pytest.fixture
def simpleStringStatistical(referenceStringDict):
	return StringStatistical(referenceStringDict)

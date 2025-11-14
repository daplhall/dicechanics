import pytest

from ttstatistics.dicechanics.statisticals.scalar import ScalarStatistical
from ttstatistics.dicechanics.statisticals.string import StringStatistical


@pytest.fixture
def emptyScalarStatistical():
	return ScalarStatistical()


@pytest.fixture
def simpleScalarStatistical(referenceStatisticalDict):
	return ScalarStatistical(referenceStatisticalDict)


@pytest.fixture
def simpleStringStatistical(referenceStringDict):
	return StringStatistical(referenceStringDict)

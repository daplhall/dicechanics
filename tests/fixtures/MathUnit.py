import pytest

from dicechanics.baseunits.combinationsunit import CombinationsUnit


@pytest.fixture
def StandardMathUnit():
	return CombinationsUnit({1: 2, 3: 4, 5.5: 2})

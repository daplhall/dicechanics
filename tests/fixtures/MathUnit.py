import pytest

from dicechanics.baseunits.CombinationsUnit import MathOpsUnit


@pytest.fixture
def StandardMathUnit():
	return MathOpsUnit({1: 2, 3: 4, 5.5: 2})

import pytest
from macros import CREATION_FACES, STANDARD_OPS_FACES

import dicechanics as ds


@pytest.fixture
def stress_die():
	return ds.d(CREATION_FACES)


@pytest.fixture
def ops_dice():
	return ds.d(STANDARD_OPS_FACES)

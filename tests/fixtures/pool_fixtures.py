import pytest

import dicechanics as ds


@pytest.fixture
def pool_1d6():
	return ds.pool([ds.d6])


@pytest.fixture
def pool_3d6():
	return ds.pool([ds.d6] * 3)

import pytest

import dicechanics as ds


@pytest.fixture
def stress_pool():
	return ds.pool([ds.d(50)] * 50)


@pytest.fixture
def stress_pool_small():
	return ds.pool([ds.d(50)] * 8)

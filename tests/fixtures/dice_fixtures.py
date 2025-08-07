import pytest

import dicechanics as ds


@pytest.fixture
def d20():
	return ds.d20


@pytest.fixture
def d10():
	return ds.d10


@pytest.fixture
def d6():
	return ds.d6


@pytest.fixture
def d4():
	return ds.d4


@pytest.fixture
def d2():
	return ds.d(2)


@pytest.fixture
def f2d6():
	return 2 @ ds.d6

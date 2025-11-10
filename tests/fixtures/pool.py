import pytest

from ttstatistics.core.pool import Pool


@pytest.fixture
def emptyPool():
	return Pool()


@pytest.fixture
def poolOneBagInside(bagWithItems):
	return Pool([bagWithItems])

import pytest

from ttstatistics.core.collection import Collection


@pytest.fixture
def emptyPool():
	return Collection()


@pytest.fixture
def poolOneBagInside(bagWithItems):
	return Collection([bagWithItems])

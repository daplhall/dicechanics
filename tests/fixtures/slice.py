import pytest

from ttstatistics.core.slice import Slice


@pytest.fixture
def emptySlice():
	return Slice()

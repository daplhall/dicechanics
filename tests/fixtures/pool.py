import pytest

from ttstatistics.dicechanics.pool import Pool


@pytest.fixture
def pool3d6(d6):
	return Pool({d6: 3})

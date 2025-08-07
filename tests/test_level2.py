import pytest

import dicechanics as ds


def test_addint(pool_1d6, d6):
	newpool = pool_1d6 + 1
	assert newpool._bag == [d6, ds.Die([1])]


def test_addfloat(pool_1d6, d6):
	newpool = pool_1d6 + 1.5
	assert newpool._bag == [d6, ds.Die([1.5])]


def test_adddice(pool_1d6, d6, d10):
	newpool = pool_1d6 + d10
	assert newpool._bag == [d6, d10]


def test_add_raise(pool_1d6, d6, d10):
	with pytest.raises(ValueError):
		pool_1d6 + "a"

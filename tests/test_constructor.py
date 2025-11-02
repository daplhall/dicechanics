import pytest

import dicechanics as ds


@pytest.fixture
def faces_d8():
	return list(range(1, 9))


@pytest.fixture
def flatcurve_d6():
	return [1] * 6


@pytest.fixture
def faces_d6():
	return list(range(1, 7))


@pytest.fixture
def faces_d4():
	return list(range(1, 5))


def test_construct_number():
	d = ds.d(5)
	assert d == ds.Die({1: 1, 2: 1, 3: 1, 4: 1, 5: 1})


def test_construct_z(flatcurve_d6):
	d = ds.z(5)
	assert d == ds.Die({0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1})


def test_construct_text1(d6):
	d = ds.d("1,2,3,4,5,6")
	assert d == d6


def test_construct_text2():
	d = ds.d("1,2,3..6,9")
	assert d == ds.Die({1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 9: 1})


def test_construct_text_count():
	d = ds.d("1,2,3,3,4")
	assert d == ds.Die({1: 1, 2: 1, 3: 2, 4: 1})


def test_construct_iterable():
	d = ds.d(range(1, 8))
	assert d == ds.Die({1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1})


def test_copy():
	d = ds.d("1..5:4,20,20,31")
	assert d == ds.Die({1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 20: 2, 31: 1})


def test_decorator():
	@ds.d("5..6:3,6,6")
	def funky_dice(face):
		if face == 1:
			return 32
		elif face == 6:
			return 42
		else:
			return -1

	d = funky_dice()
	assert d == ds.Die({-1: 3, 42: 5})


def test_decorator_explode(faces_d6):
	@ds.d(faces_d6)
	def funky_dice(face):
		if face == 6:
			return ds.d(faces_d6)
		else:
			return face

	d = funky_dice()
	assert d == ds.Die({1: 7, 2: 7, 3: 7, 4: 7, 5: 7, 6: 1})


def test_decorator_d6_to_d4(faces_d6, faces_d4):
	@ds.d(faces_d6)
	def funky_dice(face):
		if face == 6:
			return ds.d(faces_d4)
		else:
			return face

	d = funky_dice()
	assert d == ds.Die({1: 5, 2: 5, 3: 5, 4: 5, 5: 4})


def test_pool_constructor(faces_d6):
	d6 = ds.d(faces_d6)
	inpt = [d6, d6]
	pool = ds.pool(inpt)
	assert pool._bag == inpt


def test_pool_constructor_3dice(faces_d6, faces_d8):
	d6 = ds.d(faces_d6)
	d8 = ds.d(faces_d8)
	inpt = [d6, d8, d6]
	pool = ds.pool(inpt)
	assert pool._bag == inpt

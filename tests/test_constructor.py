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
	assert d.f == [1, 2, 3, 4, 5]
	assert d.c == [1] * 5


def test_construct_z(flatcurve_d6):
	d = ds.z(5)
	assert d.f == [0, 1, 2, 3, 4, 5]
	assert d.c == flatcurve_d6


def test_construct_text1(flatcurve_d6, faces_d6):
	d = ds.d("1,2,3,4,5,6")
	assert d.f == faces_d6
	assert d.c == flatcurve_d6


def test_construct_text2(flatcurve_d6, faces_d6):
	d = ds.d("1,2,3..6,9")
	assert d.f == faces_d6 + [9]
	assert d.c == flatcurve_d6 + [1]


def test_construct_text_count():
	d = ds.d("1,2,3,3,4")
	assert d.f == [1, 2, 3, 4]
	assert d.c == [1, 1, 2, 1]


def test_construct_iterable(faces_d6, flatcurve_d6):
	d = ds.d(range(1, 7))
	assert d.f == faces_d6
	assert d.c == flatcurve_d6


def test_copy():
	d = ds.d("1..5:4,20,20,31")
	g = d.copy()
	assert d.f == g.f
	assert d.c == g.c


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
	assert d.f == [-1, 42]
	assert d.c == [3, 5]


def test_decorator_explode(faces_d6):
	@ds.d(faces_d6)
	def funky_dice(face):
		if face == 6:
			return ds.d(faces_d6)
		else:
			return face

	d = funky_dice()
	assert d.f == [1, 2, 3, 4, 5, 6]
	assert d.c == [7, 7, 7, 7, 7, 1]


def test_decorator_d6_to_d4(faces_d6, faces_d4):
	@ds.d(faces_d6)
	def funky_dice(face):
		if face == 6:
			return ds.d(faces_d4)
		else:
			return face

	d = funky_dice()
	assert d.f == [1, 2, 3, 4, 5]
	assert d.c == [5, 5, 5, 5, 4]


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

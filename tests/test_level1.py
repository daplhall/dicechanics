import pytest

import dicechanics as ds


def test_plus_dice(d6):
	d = d6 + d6
	assert d.f == [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
	assert d.c == [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]


def test_plus_differnt(d6):
	g = ds.d("2,4,6,8,20")
	d = d6 + g
	assert d.f == [
		3,
		4,
		5,
		6,
		7,
		8,
		9,
		10,
		11,
		12,
		13,
		14,
		21,
		22,
		23,
		24,
		25,
		26,
	]
	assert d.c == [1, 1, 2, 2, 3, 3, 3, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1]


def test_plus_different_2(d4):
	d = ds.Die(
		[2]
		+ [3] * 2
		+ [4] * 3
		+ [5] * 4
		+ [6] * 5
		+ [7] * 6
		+ [8] * 5
		+ [9] * 4
		+ [10] * 3
		+ [11] * 2
		+ [12]
	)
	g = d4 + d
	assert g.f == [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
	assert g.c == [1, 3, 6, 10, 14, 18, 20, 20, 18, 14, 10, 6, 3, 1]


def test_matmult(d6):
	d = 2 @ d6
	assert d.f == [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
	assert d.c == [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]


def test_matmult_multiple(d6):
	d = 4 @ d6
	assert d.f == list(range(4, 24 + 1))
	assert d.c == [
		1,
		4,
		10,
		20,
		35,
		56,
		80,
		104,
		125,
		140,
		146,
		140,
		125,
		104,
		80,
		56,
		35,
		20,
		10,
		4,
		1,
	]


def test_matmult_one(d6):
	d = 1 @ d6
	assert d.f == d6.f
	assert d.c == d6.c


def test_matmult_negative(d6):
	d = -4 @ d6
	assert d.f == list(range(-24, -3))
	assert d.c == [
		1,
		4,
		10,
		20,
		35,
		56,
		80,
		104,
		125,
		140,
		146,
		140,
		125,
		104,
		80,
		56,
		35,
		20,
		10,
		4,
		1,
	]


def test_greater_than(d6):
	d = d6 > d6
	assert d.f == [0, 1]
	assert d.c == [7, 5]


def test_greater_equal_than(d6):
	d = d6 >= d6
	assert d.f == [0, 1]
	assert d.c == [5, 7]


def test_rmatmul(d2, d6):
	d = d2 @ d6
	assert d.f == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
	assert d.c == [6, 7, 8, 9, 10, 11, 6, 5, 4, 3, 2, 1]


def test_rmatmul2():
	f = ds.d("1,3,6")
	g = ds.d("4,7,8")
	d = f @ g
	assert d.f == [
		4,
		7,
		8,
		12,
		15,
		16,
		18,
		19,
		20,
		21,
		22,
		23,
		24,
		27,
		28,
		30,
		31,
		32,
		33,
		34,
		35,
		36,
		37,
		38,
		39,
		40,
		41,
		42,
		43,
		44,
		45,
		46,
		47,
		48,
	]
	assert d.c == [
		243,
		243,
		243,
		27,
		81,
		81,
		81,
		162,
		81,
		27,
		81,
		81,
		28,
		6,
		6,
		15,
		30,
		15,
		20,
		60,
		60,
		35,
		60,
		90,
		66,
		45,
		60,
		61,
		36,
		21,
		20,
		15,
		6,
		1,
	]


@pytest.mark.filterwarnings("ignore: A 0d")
def test_rmatmul3():
	f = ds.d("0,1")
	g = ds.d("1,2,3")
	D = f @ g
	assert D.f == [0, 1, 2, 3]
	assert D.c == [3, 1, 1, 1]


def test_dice_nroll_raise(d6):
	with pytest.raises(ValueError):
		"a" @ d6
	with pytest.raises(ValueError):
		d6 @ "a"

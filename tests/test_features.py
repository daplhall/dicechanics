import pytest

import dicechanics as ds


@pytest.fixture
def folding_faces():
	return [3, 4, 5, 6, 7, 8, 9, 10]


def test_reroll1(d6):
	d = d6.reroll(6)
	assert d.f == d6.f
	assert d.c == [7] * 5 + [1]


def test_reroll2(d6):
	d = 2 @ d6
	g = d.reroll(7)
	assert g.f == d.f
	assert g.c == [7, 14, 21, 28, 35, 6, 35, 28, 21, 14, 7]


def test_reroll3(d6):
	d = 3 @ d6
	g = d.reroll(7)
	assert d.f == g.f
	assert g.c == [
		77,
		231,
		462,
		770,
		75,
		1617,
		1925,
		2079,
		2079,
		1925,
		1617,
		1155,
		770,
		462,
		231,
		77,
	]


def test_reroll_depth(d6):
	d = d6.reroll(5, 6, depth=2)
	assert d.f == d6.f
	assert d.c == [13, 13, 13, 13, 1, 1]


def test_reroll_depth2(d10):
	d = d10.reroll(1, 4, 6, 8, 10, depth=6)
	assert d.f == d10.f
	assert d.c == [1, 127, 127, 1, 127, 1, 127, 1, 127, 1]


def test_reroll_inf(d10, d6):
	d = d10.reroll(7, 8, 9, 10, depth="inf")
	assert d.f == d6.f
	assert d.c == [1] * 6


def test_count1(d10):
	d = d10.count(5, 6)
	assert d.f == [0, 1]
	assert d.c == [4, 1]


def test_explode(d6):
	d = d6.explode(6)
	assert d.f == [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]
	assert d.c == [6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1]


def test_explode_double(d6):
	d = d6.explode(5, 6)
	assert d.f == [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]
	assert d.c == [6, 6, 6, 6, 1, 2, 2, 2, 2, 2, 1]


def test_explode_depth(d6):
	d = d6.explode(6, depth=3)
	assert d.f == [
		1,
		2,
		3,
		4,
		5,
		7,
		8,
		9,
		10,
		11,
		13,
		14,
		15,
		16,
		17,
		19,
		20,
		21,
		22,
		23,
		24,
	]
	assert d.c == [
		216,
		216,
		216,
		216,
		216,
		36,
		36,
		36,
		36,
		36,
		6,
		6,
		6,
		6,
		6,
		1,
		1,
		1,
		1,
		1,
		1,
	]


def test_explode_depth2(d6):
	d = d6.explode(5, 6, depth=2)
	assert d.f == [
		1,
		2,
		3,
		4,
		6,
		7,
		8,
		9,
		10,
		11,
		12,
		13,
		14,
		15,
		16,
		17,
		18,
	]
	assert d.c == [36, 36, 36, 36, 6, 12, 12, 12, 6, 1, 3, 4, 4, 4, 4, 3, 1]


def test_implode(d6):
	d = d6.implode(1)
	assert d.f == [-5, -4, -3, -2, -1, 0, 2, 3, 4, 5, 6]
	assert d.c == [1, 1, 1, 1, 1, 1, 6, 6, 6, 6, 6]


def test_fold_under(d10, folding_faces):
	d = d10.fold_under(3)
	assert d.f == folding_faces
	assert d.c == [3, 1, 1, 1, 1, 1, 1, 1]


def test_fold_under_into(d10, folding_faces):
	d = d10.fold_under(3, into=4)
	assert d.f == folding_faces
	assert d.c == [1, 3, 1, 1, 1, 1, 1, 1]


def test_fold_under_into_0(d10, folding_faces):
	d = d10.fold_under(3, into=0)
	assert d.f == [0] + folding_faces
	assert d.c == [2, 1, 1, 1, 1, 1, 1, 1, 1]


def test_string(d6):
	assert (
		str(d6)
		=='Die with mu - 3.50, sigma - 1.71\n--------------------------------\n1|#################### 16.67%\n2|#################### 16.67%\n3|#################### 16.67%\n4|#################### 16.67%\n5|#################### 16.67%\n6|#################### 16.67%\n'
	)


def test_pool_string(d6):
	pool = ds.pool([d6, d6])
	assert (
		str(pool) == "Pool([Die({1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}),"
		" Die({1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1})])"
	)

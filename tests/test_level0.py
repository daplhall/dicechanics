import dicechanics as ds


def test_plus_int(d6):
	d = d6 + 1
	assert d.f == [2, 3, 4, 5, 6, 7]
	assert d.c == d6.c


def test_plus_float(d6):
	d = d6 + 0.5
	assert d.f == [1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
	assert d.c == d6.c


def test_sub_int(d6):
	d = d6 - 1
	assert d.f == [0, 1, 2, 3, 4, 5]
	assert d.c == d6.c


def test_rsub_int(d6):
	d = 1 - d6
	assert d.f == [-5, -4, -3, -2, -1, 0]
	assert d.c == d6.c


def test_mult_int(d6):
	d = d6 * 2
	assert d.f == [2, 4, 6, 8, 10, 12]
	assert d.c == d6.c


def test_mult_float(d6):
	d = d6 * 1.5
	assert d.f == [1.5, 3.0, 4.5, 6.0, 7.5, 9.0]
	assert d.c == d6.c


def test_divide_int(d6):
	d = d6 / 2
	assert d.f == [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
	assert d.c == d6.c


def test_divide_int_roundup():
	d6 = ds.d(6, rounding=ds.ops.ceil)
	d = d6 / 2
	assert d.f == [1, 2, 3]
	assert d.c == [1] * 3


def test_divide_int_rounddown():
	d6 = ds.d(6, rounding=ds.ops.floor)
	d = d6 / 2
	assert d.f == [0, 1, 2, 3]
	assert d.c == [1, 2, 2, 1]


def test_divide_int_floor(d6):
	d6 = d6
	d = d6 // 2
	assert d.f == [0, 1, 2, 3]
	assert d.c == [1, 2, 2, 1]


def test_divide_float(d6):
	d = d6 / 1.5
	for df, rf in zip(d.f, [0.67, 1.33, 2.0, 2.67, 3.33, 4.0]):
		assert round(df, 2) == rf
	assert d.c == d6.c


def test_neg(d6):
	g = -d6
	assert g.f == [-6, -5, -4, -3, -2, -1]
	assert g.c == d6.c


def test_pos(d6):
	g = +d6
	assert g.f == [1, 2, 3, 4, 5, 6]
	assert g.c == d6.c


def test_greater_than(d10):
	d = d10 > 8
	assert d.f == [0, 1]
	assert d.c == [4, 1]


def test_greater_eqaual_than(d10):
	d = d10 >= 8
	assert d.f == [0, 1]
	assert d.c == [7, 3]


def test_less_than(d10):
	d = d10 < 3
	assert d.f == [0, 1]
	assert d.c == [4, 1]


def test_less_equal_than(d10):
	d = d10 <= 3
	assert d.f == [0, 1]
	assert d.c == [7, 3]


def test_not_equal(d10):
	d = d10 != d10
	assert not d


def test_equal(d10):
	d = d10 == d10
	assert d

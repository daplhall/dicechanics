import dicechanics as ds


def test_plus_int(d6):
	d = d6 + 1
	assert d == ds.Die(dict(zip([2, 3, 4, 5, 6, 7], [1, 1, 1, 1, 1, 1])))


def test_plus_float(d6):
	d = d6 + 0.5
	assert d == ds.Die(dict(zip([1.5, 2.5, 3.5, 4.5, 5.5, 6.5], [1] * 6)))


def test_sub_int(d6):
	d = d6 - 1
	assert d == ds.Die(dict(zip([0, 1, 2, 3, 4, 5], [1] * 6)))


def test_rsub_int(d6):
	d = 1 - d6
	assert d == ds.Die(dict(zip([-5, -4, -3, -2, -1, 0], [1] * 6)))


def test_mult_int(d6):
	d = d6 * 2
	assert d == ds.Die(dict(zip([2, 4, 6, 8, 10, 12], [1] * 6)))


def test_mult_float(d6):
	d = d6 * 1.5
	assert d == ds.Die(dict(zip([1.5, 3.0, 4.5, 6.0, 7.5, 9.0], [1] * 6)))


def test_divide_int(d6):
	d = d6 / 2
	assert d == ds.Die(dict(zip([0.5, 1.0, 1.5, 2.0, 2.5, 3.0], [1] * 6)))


def test_divide_int_floor(d6):
	d6 = d6
	d = d6 // 2
	assert d == ds.Die(dict(zip([0, 1, 2, 3], [1, 2, 2, 1])))


def test_divide_float(d6):
	d = d6 / 1.5
	for df, rf in zip(d.f, [0.67, 1.33, 2.0, 2.67, 3.33, 4.0]):
		assert round(df, 2) == rf


def test_neg(d6):
	g = -d6
	assert g.f == [-6, -5, -4, -3, -2, -1]


def test_pos(d6):
	g = +d6
	assert g.f == [1, 2, 3, 4, 5, 6]


def test_greater_than(d10):
	d = d10 > 8
	assert d == ds.Die(dict(zip([0, 1], [4, 1])))


def test_greater_eqaual_than(d10):
	d = d10 >= 8
	assert d == ds.Die(dict(zip([0, 1], [7, 3])))


def test_less_than(d10):
	d = d10 < 3
	assert d == ds.Die(dict(zip([0, 1], [4, 1])))


def test_less_equal_than(d10):
	d = d10 <= 3
	assert d == ds.Die(dict(zip([0, 1], [7, 3])))


def test_not_equal(d10):
	d = d10 != d10
	assert not d


def test_equal(d10):
	d = d10 == d10
	assert d


def test_rmul(d6):
	d = 2 * d6
	assert d == ds.Die(dict(zip([2, 4, 6, 8, 10, 12], [1, 1, 1, 1, 1, 1])))

import dicechanics as ds


def test_perform(pool_3d6, d6):
	d = pool_3d6.perform(ds.ops.add)
	assert d.f == [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
	assert d.c == [1, 3, 6, 10, 15, 21, 25, 27, 27, 25, 21, 15, 10, 6, 3, 1]


def test_perform_decorator(pool_3d6):
	@pool_3d6
	def newdice(x, y):
		return x + y

	d = newdice()
	assert d.f == [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
	assert d.c == [1, 3, 6, 10, 15, 21, 25, 27, 27, 25, 21, 15, 10, 6, 3, 1]


def test_mult_non_selective(pool_3d6):
	d = pool_3d6.perform(ds.ops.mul)
	assert d.f == [
		1,
		2,
		3,
		4,
		5,
		6,
		8,
		9,
		10,
		12,
		15,
		16,
		18,
		20,
		24,
		25,
		27,
		30,
		32,
		36,
		40,
		45,
		48,
		50,
		54,
		60,
		64,
		72,
		75,
		80,
		90,
		96,
		100,
		108,
		120,
		125,
		144,
		150,
		180,
		216,
	]
	assert d.c == [
		1,
		3,
		3,
		6,
		3,
		9,
		7,
		3,
		6,
		15,
		6,
		6,
		9,
		9,
		15,
		3,
		1,
		12,
		3,
		12,
		6,
		3,
		9,
		3,
		3,
		12,
		1,
		9,
		3,
		3,
		6,
		3,
		3,
		3,
		6,
		1,
		3,
		3,
		3,
		1,
	]


def test_max_non_selective(pool_3d6):
	d = pool_3d6.perform(max)
	assert d.f == [1, 2, 3, 4, 5, 6]
	assert d.c == [1, 7, 19, 37, 61, 91]


def test_min_non_selective(pool_3d6):
	d = pool_3d6.perform(min)
	assert d.f == [1, 2, 3, 4, 5, 6]
	assert d.c == [1, 7, 19, 37, 61, 91][::-1]


def test_perform_selective(pool_3d6):
	d = pool_3d6[1:].perform(ds.ops.add)
	assert d.f == [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
	assert d.c == [1, 3, 7, 12, 19, 27, 34, 36, 34, 27, 16]


def test_selective_add_middle_mixed():
	pool = ds.Pool([ds.d4, ds.d6, ds.d8])
	d = pool[0, 1, 0].perform(ds.ops.add)
	assert d.f == [1, 2, 3, 4, 5, 6]
	assert d.c == [4, 10, 13, 13, 5, 3]


def test_selective_add_with_numbers():
	pool = ds.Pool([ds.d4, 3])
	d = pool[0, 1].perform(ds.ops.add)
	assert d.f == [3, 4]
	assert d.c == [3, 1]

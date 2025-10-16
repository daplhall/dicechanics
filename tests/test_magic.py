import dicechanics as ds


def test_dice_iterator():
	d = ds.d("1..3:2")
	res = [1, 2, 3]
	for i, j in zip(d, res):
		assert i == j


def test_dice_contains(d6):
	assert 6 in d6


def test_boolean_dice():
	f = ds.d(6)
	g = ds.d(6)
	assert f is not g
	assert g == f


def test_hashable_dice(d6):
	f = {"a": d6}
	assert f["a"] == d6

import pytest

import dicechanics as ds


@pytest.fixture
def folding_under_faces():
	return [3, 4, 5, 6, 7, 8, 9, 10]


@pytest.fixture
def folding_over_faces():
	return [1, 2, 3, 4, 5, 6, 7, 8]


def test_reroll1(d6):
	d = d6.reroll(6)
	assert d == ds.Die({1: 7, 2: 7, 3: 7, 4: 7, 5: 7, 6: 1})


def test_reroll2(d6):
	d = 2 @ d6
	g = d.reroll(7)
	assert g == ds.Die(
		{
			2: 7,
			3: 14,
			4: 21,
			5: 28,
			6: 35,
			7: 6,
			8: 35,
			9: 28,
			10: 21,
			11: 14,
			12: 7,
		}
	)


def test_reroll3(d6):
	d = 3 @ d6
	g = d.reroll(7)
	assert g == ds.Die(
		{
			3: 77,
			4: 231,
			5: 462,
			6: 770,
			7: 75,
			8: 1617,
			9: 1925,
			10: 2079,
			11: 2079,
			12: 1925,
			13: 1617,
			14: 1155,
			15: 770,
			16: 462,
			17: 231,
			18: 77,
		}
	)


def test_reroll_depth(d6):
	d = d6.reroll(5, 6, depth=2)
	assert d == ds.Die({1: 13, 2: 13, 3: 13, 4: 13, 5: 1, 6: 1})


def test_reroll_depth2(d10):
	d = d10.reroll(1, 4, 6, 8, 10, depth=6)
	assert d == ds.Die(
		{
			1: 1,
			2: 127,
			3: 127,
			4: 1,
			5: 127,
			6: 1,
			7: 127,
			8: 1,
			9: 127,
			10: 1,
		}
	)


def test_reroll_inf(d10, d6):
	d = d10.reroll(7, 8, 9, 10, depth="inf")
	assert d == ds.Die({1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1})


def test_count1(d10):
	d = d10.count(5, 6)
	assert d == ds.Die({0: 4, 1: 1})


def test_explode(d6):
	d = d6.explode(6)
	assert d == ds.Die(
		dict(
			zip(
				[1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12],
				[6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
			)
		)
	)


def test_explode_double(d6):
	d = d6.explode(5, 6)

	assert d == ds.Die(
		dict(
			zip(
				[1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12],
				[6, 6, 6, 6, 1, 2, 2, 2, 2, 2, 1],
			)
		)
	)


def test_explode_depth(d6):
	d = d6.explode(6, depth=3)
	assert d == ds.Die(
		dict(
			zip(
				[
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
				],
				[
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
				],
			)
		)
	)


def test_explode_depth2(d6):
	d = d6.explode(5, 6, depth=2)
	assert ds.Die(
		dict(
			zip(
				[1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
				[36, 36, 36, 36, 6, 12, 12, 12, 6, 1, 3, 4, 4, 4, 4, 3, 1],
			)
		)
	)


def test_implode(d6):
	d = d6.implode(1)
	d == ds.Die(
		dict(
			zip(
				[-5, -4, -3, -2, -1, 0, 2, 3, 4, 5, 6],
				[1, 1, 1, 1, 1, 1, 6, 6, 6, 6, 6],
			)
		)
	)


def test_fold_under(d10, folding_under_faces):
	d = d10.fold_under(3)
	assert d == ds.Die(dict(zip(folding_under_faces, [3, 1, 1, 1, 1, 1, 1, 1])))


def test_fold_under_into(d10, folding_under_faces):
	d = d10.fold_under(3, into=4)
	assert d == ds.Die(dict(zip(folding_under_faces, [1, 3, 1, 1, 1, 1, 1, 1])))


def test_fold_under_into_0(d10, folding_under_faces):
	d = d10.fold_under(3, into=0)
	assert d == ds.Die(
		dict(zip([0] + folding_under_faces, [2, 1, 1, 1, 1, 1, 1, 1, 1]))
	)


def test_fold_over(d10, folding_over_faces):
	d = d10.fold_over(8)
	assert d == ds.Die(dict(zip(folding_over_faces, [1, 1, 1, 1, 1, 1, 1, 3])))


def test_fold_over_into(d10, folding_over_faces):
	d = d10.fold_over(8, into=7)
	assert d == ds.Die(dict(zip(folding_over_faces, [1, 1, 1, 1, 1, 1, 3, 1])))


def test_fold_over_into_0(d10, folding_over_faces):
	d = d10.fold_over(8, into=0)
	assert d == ds.Die(
		dict(zip([0] + folding_over_faces, [2, 1, 1, 1, 1, 1, 1, 1, 1]))
	)


def test_dice_max(f2d6):
	d = f2d6
	assert d.max == 12


def test_dice_min(f2d6):
	d = f2d6
	assert d.min == 2


def test_dice_var(f2d6):
	d = f2d6
	assert d.variance == 5.833333333333333


def test_dice_std(f2d6):
	d = f2d6
	assert d.std == 2.41522945769824


def test_dice_cfd(f2d6):
	d = f2d6
	assert d.cdf == [
		0.027777777777777776,
		0.08333333333333333,
		0.16666666666666666,
		0.2777777777777778,
		0.4166666666666667,
		0.5833333333333334,
		0.7222222222222223,
		0.8333333333333335,
		0.9166666666666669,
		0.9722222222222224,
		1.0000000000000002,
	]


def test_string(d6):
	assert (
		str(d6)
		== "Die with mu - 3.50, sigma - 1.71, faces - 6\n-------------------------------------------\n1|#################### 16.67%\n2|#################### 16.67%\n3|#################### 16.67%\n4|#################### 16.67%\n5|#################### 16.67%\n6|#################### 16.67%\n"
	)


def test_pool_string(d6):
	pool = ds.pool([d6, d6])
	assert (
		str(pool) == "Pool([Die({1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}),"
		" Die({1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1})])"
	)


def test_dice_expansion():
	d = ds.d({1: 1, 2: 1, 3: 1, 4: 1})
	p = ds.d({2: 1, 1: 2, d: 1})
	res = ds.d({1: 9, 2: 5, 3: 1, 4: 1})
	assert p == res

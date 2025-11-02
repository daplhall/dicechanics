import math

from dicechanics.baseunits.statisticalunit import StatUnitNum, StatUnitStr


def test_create():
	sunit = StatUnitNum({1: 2, 3: 4, 5.5: 2})
	assert sunit.p == [2 / 8, 4 / 8, 2 / 8]
	assert sunit.c == [2, 4, 2]
	assert sunit.o == [1, 3, 5.5]
	assert sunit.cdf == [2 / 8, 6 / 8, 1]


def test_create_str():
	sunit = StatUnitStr({"ab": 4, "bc": 2, "ba": 4, "cb": 2})
	assert sunit.o == ["ab", "bc"]
	assert sunit.p == [8 / 12, 4 / 12]


def test_numbers():
	sunit = StatUnitNum({1: 2, 3: 4, 5.5: 2})
	refmean = 2 / 8 * 1 + 4 / 8 * 3 + 2 / 8 * 5.5
	assert sunit.mean == refmean
	refvar = (
		2 / 8 * (1 - refmean) ** 2
		+ 4 / 8 * (3 - refmean) ** 2
		+ 2 / 8 * (5.5 - refmean) ** 2
	)
	assert sunit.variance == refvar
	assert sunit.std == math.sqrt(refvar)


def test_maxmin_numbers():
	sunit = StatUnitNum({1: 2, 3: 4, 5.5: 2})
	assert sunit.max == 5.5
	assert sunit.min == 1


def test_simplify():
	sunit = StatUnitNum({1: 2, 3: 4, 5.5: 2})
	sunit.simplify()
	assert sunit.c == [1, 2, 1]

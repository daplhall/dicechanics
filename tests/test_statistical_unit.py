import math

from dicechanics.baseunits.statistical_unit import StatisticalUnit


def test_create():
	sunit = StatisticalUnit({1: 2, 3: 4, 5.5: 2})
	assert sunit.p == [2 / 8, 4 / 8, 2 / 8]
	assert sunit.c == [2, 4, 2]
	assert sunit.o == [1, 3, 5.5]
	assert sunit.cdf == [2 / 8, 6 / 8, 1]


def test_numbers():
	sunit = StatisticalUnit({1: 2, 3: 4, 5.5: 2})
	refmean = 2 / 8 * 1 + 4 / 8 * 3 + 2 / 8 * 5.5
	assert sunit.mean == refmean
	refvar = (
		2 / 8 * (1 - refmean) ** 2
		+ 4 / 8 * (3 - refmean) ** 2
		+ 2 / 8 * (5.5 - refmean) ** 2
	)
	assert sunit.varians == refvar
	assert sunit.std == math.sqrt(refvar)


def test_nan():
	sunit = StatisticalUnit({"a": 2, "b": 4, "c": 2})
	assert sunit.p == [2 / 8, 4 / 8, 2 / 8]
	assert sunit.c == [2, 4, 2]
	assert sunit.o == ["a", "b", "c"]
	assert sunit.mean is None
	assert sunit.varians is None
	assert sunit.std is None


def test_objects():
	sunit = StatisticalUnit({"a": 2, (1, 2): 4, 5.4: 2})
	assert sunit.p == [2 / 8, 4 / 8, 2 / 8]
	assert sunit.c == [2, 4, 2]
	assert sunit.o == ["a", (1, 2), 5.4]
	assert sunit.mean is None
	assert sunit.varians is None
	assert sunit.std is None


def test_maxmin_objects():
	sunit = StatisticalUnit({"a": 2, (1, 2): 4, 5.4: 2})
	assert sunit.max is None
	assert sunit.min is None


def test_maxmin_numbers():
	sunit = StatisticalUnit({1: 2, 3: 4, 5.5: 2})
	assert sunit.max == 5.5
	assert sunit.min == 1


def test_simplify():
	sunit = StatisticalUnit({1: 2, 3: 4, 5.5: 2})
	sunit.simplify()
	assert sunit.c == [1, 2, 1]

import pytest
from groups import group_die_features
from macros import CREATION_FACES

import dicechanics as ds


def explode():
	return ds.d10.explode(10, depth=6)


def reroll():
	return ds.d10.reroll(10, depth=6)


@group_die_features
@pytest.mark.parametrize("inpt", [explode, reroll])
def bm_unique_mechanics(inpt, benchmark):
	res = benchmark(inpt)
	assert res.units == 10000000


def count(d):
	return d.count(list(range(CREATION_FACES // 2)))


def map(d):
	@d
	def die_filter(face):
		if face < CREATION_FACES // 2:
			return 0
		else:
			return 1

	return die_filter()


@group_die_features
@pytest.mark.parametrize("inpt", [count, map])
def bm_modify(inpt, benchmark, stress_die):
	d = stress_die
	res = benchmark(inpt, d)
	assert res.units == CREATION_FACES


def cumulative(d):
	return d.cdf


@group_die_features
def bm_cumulative(benchmark, stress_die):
	d = stress_die
	res = benchmark(cumulative, d)
	assert res[0] == 0.0001


def copy(d):
	return d.copy()


@group_die_features
def bm_die_copy(stress_die, benchmark):
	d = stress_die
	res = benchmark(copy, d)
	assert res == d

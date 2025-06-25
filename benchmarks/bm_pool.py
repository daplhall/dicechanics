import pytest
from groups import group_multiple_dice

import dicechanics as ds


def pool_nonselective_add(p):
	return p.perform(ds.ops.add)


def pool_nonselective_max(p):
	return p.perform(ds.ops.max)


# TODO once the selective is optimized, we paramterize this test
@group_multiple_dice
@pytest.mark.parametrize("pool", [pool_nonselective_max, pool_nonselective_add])
def bm_pool_nonselective(pool, stress_pool, benchmark):
	p = stress_pool
	res = benchmark(pool, p)
	assert (
		res._units
		== 8881784197001252323389053344726562500000000000000000000000000000000000000000000000000  # noqa: E501
	)


# -----TEMP----
def pool_selective(p):
	return p[3:].perform(ds.ops.add)


@group_multiple_dice
def bm_pool_selective(stress_pool_small, benchmark):
	p = stress_pool_small
	res = benchmark(pool_selective, p)
	assert res._units == 39062500000000

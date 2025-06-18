import pytest

import dicechanics as ds


def pool_nonselective_add():
	return ds.pool([ds.d(50)] * 50).perform(ds.ops.add)


def pool_nonselective_max():
	return ds.pool([ds.d(50)] * 50).perform(ds.ops.max)


# TODO once the selective is optimized, we paramterize this test
@pytest.mark.parametrize("pool", [pool_nonselective_max, pool_nonselective_add])
def bm_pool_nonselective(pool, benchmark):
	res = benchmark(pool)
	assert (
		res._units
		== 8881784197001252323389053344726562500000000000000000000000000000000000000000000000000  # noqa: E501
	)


# -----TEMP----
def pool_selective():
	return ds.pool([ds.d(50)] * 8)[3:].perform(ds.ops.add)


def bm_pool_selective(benchmark):
	res = benchmark(pool_selective)
	assert res._units == 39062500000000

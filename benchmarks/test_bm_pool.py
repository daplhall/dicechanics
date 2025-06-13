import dicechanics as ds


def pool_nonselective():
	return ds.pool([ds.d(50)] * 50).perform(ds.ops.add)


# TODO once the selective is optimized, we paramterize this test
def test_pool_nonselective(benchmark):
	res = benchmark(pool_nonselective)
	assert (
		res._units
		== 8881784197001252323389053344726562500000000000000000000000000000000000000000000000000  # noqa: E501
	)


# -----TEMP----
def pool_selective():
	return ds.pool([ds.d(50)] * 8)[3:].perform(ds.ops.add)


def test_pool_selective(benchmark):
	res = benchmark(pool_selective)
	assert res._units == 39062500000000

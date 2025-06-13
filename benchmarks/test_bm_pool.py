import dicechanics as ds


def pool_selective():
	return ds.pool([ds.d(50)] * 50).perform(ds.ops.add)


def test_pool_selective(benchmark):
	res = benchmark(pool_selective)
	assert (
		res._units
		== 8881784197001252323389053344726562500000000000000000000000000000000000000000000000000  # noqa: E501
	)

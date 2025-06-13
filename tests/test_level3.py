import dicechanics as ds


def test_addpool(pool_1d6, d6, d10, d20):
	newpool = pool_1d6 + ds.pool([d10, d20])
	assert newpool._bag == [d6, d10, d20]

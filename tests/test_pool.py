from ttstatistics.core import protocols


def test_EmptyOnInitialzie(emptyPool):
	assert not emptyPool


def test_PoolWithBagInside(poolOneBagInside):
	assert poolOneBagInside


def test_PeakingInsideThePool(poolOneBagInside):
	assert all(
		isinstance(i, protocols.Bag) for i in poolOneBagInside.peekInside()
	)

def test_AddDieOnInit(poolOneLength):
	assert poolOneLength
	assert len(poolOneLength) == 1


def test_AddMultipleDice(poolTwoLength):
	assert poolTwoLength
	assert len(poolTwoLength) == 2


def test_EmptyInit(emptyPool):
	assert not emptyPool


def test_CombiningPools(poolTwoLength, poolOneLength):
	p = poolTwoLength + poolOneLength
	assert len(p) == 3


def test_CombiningThreePools(poolOneLength, poolTwoLength):
	p = poolTwoLength + poolTwoLength + poolOneLength
	assert len(p) == 5


def test_PoolPlusDieMakesPool(emptyDie, emptyPool):
	pool = emptyPool + emptyDie
	assert len(pool)

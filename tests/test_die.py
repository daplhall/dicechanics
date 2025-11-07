from dicechanics.pool import Pool


def test_EmptyInit(emptyDie):
	assert not emptyDie


def test_TwoDieMakeAPool(emptyDie):
	pool = emptyDie + emptyDie
	assert isinstance(pool, Pool)

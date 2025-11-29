from ttstatistics.dicechanics.pool import Pool


class PoolSpy(Pool):
	def inside(self):
		return self.internalMappings


def test_extendPool(d4):
	pool = PoolSpy({d4: 1})
	pool.extend(d4)
	assert pool.inside() == {d4: 2}


def test_addingPools(d4, d6):
	d4Pool = PoolSpy({d4: 5})
	d6Pool = PoolSpy({d6: 3})
	pool = d6Pool + d4Pool
	assert pool.inside() == {d6: 3, d4: 5}


def test_MatmultOne(d6):
	assert 1 @ d6 == PoolSpy({d6: 1})


def test_MatmultTwo(d6):
	assert 2 @ d6 == PoolSpy({d6: 2})

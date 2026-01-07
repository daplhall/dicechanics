from ttstatistics.core.operations import (
	add,
	max,
	mul,
	regularOnGroup,
	selectiveOnGroup,
)

# from ttstatistics.dicechanics.operations import perform, sum
from ttstatistics.dicechanics import operations as ops
from ttstatistics.dicechanics.die import Die


class DieSpy(Die):
	def inside(self):
		return self.internals.probability


def compareTwoFloatDict(res, ref):
	for k, v in res.items():
		assert abs(ref[k] - v) < 1e-15


def test_PerformPoolAdd(pool3d6, d6):
	res = ops.perform(pool3d6, add)
	ref = d6 + d6 + d6
	compareTwoFloatDict(res, DieSpy(ref).inside())


def test_PerformPoolMax(pool3d6, d6):
	res = ops.perform(pool3d6, max)
	ref = regularOnGroup(pool3d6, max)
	compareTwoFloatDict(res, ref)


def test_PerformAddSelective(pool3d6):
	pool = pool3d6 & (1, 2)
	res = ops.perform(pool, add)
	ref = selectiveOnGroup(pool, add)
	compareTwoFloatDict(res, ref)


def test_SumRegular(pool3d6):
	res = ops.sum(pool3d6)
	ref = regularOnGroup(pool3d6, add)
	compareTwoFloatDict(res, ref)


def test_SumSelective(pool3d6):
	pool = pool3d6 & (1, 2)
	res = ops.sum(pool)
	ref = selectiveOnGroup(pool, add)
	compareTwoFloatDict(res, ref)


def test_MulRegular(pool3d6):
	res = ops.mult(pool3d6)
	ref = regularOnGroup(pool3d6, mul)
	compareTwoFloatDict(res, ref)


def test_MulSelective(pool3d6):
	pool = pool3d6 & (1, 2)
	res = ops.mult(pool)
	ref = selectiveOnGroup(pool, mul)
	compareTwoFloatDict(res, ref)


def test_MaxRegular(pool3d6):
	res = ops.max(pool3d6)
	ref = regularOnGroup(pool3d6, max)
	compareTwoFloatDict(res, ref)


def test_MaxSelective(pool3d6):
	pool = pool3d6 & (1, 2)
	res = ops.max(pool)
	ref = selectiveOnGroup(pool, max)
	compareTwoFloatDict(res, ref)


def test_MinRegular(pool3d6):
	res = ops.min(pool3d6)
	ref = regularOnGroup(pool3d6, min)
	compareTwoFloatDict(res, ref)


def test_MinSelective(pool3d6):
	pool = pool3d6 & (1, 2)
	res = ops.min(pool)
	ref = selectiveOnGroup(pool, min)
	compareTwoFloatDict(res, ref)


def test_AdBSelective(d4, d6):
	res = ops.sum((d4 @ d6)[:])
	ref = Die(
		{
			ops.sum(1 @ d6): 1 / 4,
			ops.sum(2 @ d6): 1 / 4,
			ops.sum(3 @ d6): 1 / 4,
			ops.sum(4 @ d6): 1 / 4,
		}
	)
	compareTwoFloatDict(res, DieSpy(ref).inside())


def test_AdBSelectiveSlice(d4, d6):
	res = ops.sum((d4 @ d6)[:2])
	ref = Die(
		{
			ops.sum((1 @ d6)[:2]): 1 / 4,
			ops.sum((2 @ d6)[:2]): 1 / 4,
			ops.sum((3 @ d6)[:2]): 1 / 4,
			ops.sum((4 @ d6)[:2]): 1 / 4,
		}
	)
	compareTwoFloatDict(res, DieSpy(ref).inside())


def test_AdBRegular(d4, d6):
	res = ops.sum(d4 @ d6)
	ref = Die(
		{
			ops.sum(1 @ d6): 1 / 4,
			ops.sum(2 @ d6): 1 / 4,
			ops.sum(3 @ d6): 1 / 4,
			ops.sum(4 @ d6): 1 / 4,
		}
	)
	compareTwoFloatDict(res, DieSpy(ref).inside())

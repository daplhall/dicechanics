import pytest
from groups import group_multiple_dice, group_ops

import dicechanics as ds


def matmult(n, d):  # TODO Remove d50 from test i need to test onlt 50@
	return n @ d


@group_multiple_dice
def bm_matmult(d50, benchmark):
	d = d50
	res = benchmark(matmult, 50, d)
	assert (
		res._units
		== 8881784197001252323389053344726562500000000000000000000000000000000000000000000000000  # noqa: E501
	)


def dice_add(d):
	return d + d


def dice_sub(d):
	return d - d


def dice_mul(d):
	return d * d


def dice_div(d):
	return d / d


def dice_add_pool(d):
	"""
	For comparison with the add operator
	"""
	return ds.pool([d, d]).perform(ds.ops.add)


@group_ops
@pytest.mark.parametrize("inpt", [dice_add, dice_add_pool, dice_sub])
def bm_binary_ops(inpt, ops_dice, benchmark):
	d = ops_dice
	res = benchmark(inpt, d)
	assert res._units == 25000000


@group_ops
@pytest.mark.parametrize("inpt", [dice_mul, dice_div])
def bm_binary_ops_2(inpt, benchmark):
	d = ds.d(1500)
	res = benchmark(inpt, d)
	assert res._units == 2250000

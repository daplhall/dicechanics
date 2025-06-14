import pytest

import dicechanics as ds

CREATION_FACES = 10000
STANDARD_OPS_FACES = 5000


def die_from_number():
	return ds.d(CREATION_FACES)


def die_from_iterable():
	return ds.d(range(1, CREATION_FACES + 1))


def die_from_text():
	return ds.d(f"1..{CREATION_FACES}")


@pytest.mark.parametrize(
	"creator", [die_from_number, die_from_iterable, die_from_text]
)
def test_die_creation(creator, benchmark):
	res = benchmark(creator)
	assert list(res.keys()) == list(range(1, CREATION_FACES + 1))


def matmult():
	return 50 @ ds.d(50)


def test_matmult(benchmark):
	res = benchmark(matmult)
	assert (
		res._units
		== 8881784197001252323389053344726562500000000000000000000000000000000000000000000000000  # noqa: E501
	)


def dice_add():
	d = ds.d(STANDARD_OPS_FACES)
	return d + d


def dice_add_pool():
	d = ds.d(STANDARD_OPS_FACES)
	return ds.pool([d, d]).perform(ds.ops.add)


@pytest.mark.parametrize("inpt", [dice_add, dice_add_pool])
def test_add(inpt, benchmark):
	res = benchmark(inpt)
	assert res._units == 25000000

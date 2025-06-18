import pytest

import dicechanics as ds

CREATION_FACES = 10000
STANDARD_OPS_FACES = 5000


@pytest.fixture
def stress_die():
	return ds.d(CREATION_FACES)


@pytest.fixture
def ops_dice():
	return ds.d(STANDARD_OPS_FACES)


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


def matmult():  # TODO Remove d50 from test i need to test onlt 50@
	return 50 @ ds.d(50)


def test_matmult(benchmark):
	res = benchmark(matmult)
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


@pytest.mark.parametrize(
	"inpt", [dice_add, dice_add_pool, dice_sub, dice_mul, dice_div]
)
def test_add(inpt, ops_dice, benchmark):
	d = ops_dice
	res = benchmark(inpt, d)
	assert res._units == 25000000


def explode():
	return ds.d10.explode(10, depth=6)


def reroll():
	return ds.d10.reroll(10, depth=6)


@pytest.mark.parametrize("inpt", [explode, reroll])
def test_unique_mechanics(inpt, benchmark):
	res = benchmark(inpt)
	assert res._units == 10000000


def count(d):
	return d.count(list(range(CREATION_FACES // 2)))


def map(d):
	@d
	def die_filter(face):
		if face < CREATION_FACES // 2:
			return 0
		else:
			return 1

	return die_filter()


@pytest.mark.parametrize("inpt", [count, map])
def test_modify(inpt, benchmark, stress_die):
	d = stress_die
	res = benchmark(inpt, d)
	assert res._units == CREATION_FACES


def cumulative(d):
	return d.cdf


def test_cumulative(benchmark, stress_die):
	d = stress_die
	res = benchmark(cumulative, d)
	assert res[0] == 0.0001


def copy(d):
	return d.copy()


def test_die_copy(stress_die, benchmark):
	d = stress_die
	res = benchmark(copy, d)
	assert res == d

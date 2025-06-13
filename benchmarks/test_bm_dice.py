import pytest

import dicechanics as ds

NUMBER_FACES = 10000


def die_from_number():
	return ds.d(NUMBER_FACES)


def die_from_iterable():
	return ds.d(range(1, NUMBER_FACES + 1))


def die_from_text():
	return ds.d(f"1..{NUMBER_FACES}")


@pytest.mark.parametrize(
	"creator", [die_from_number, die_from_iterable, die_from_text]
)
def test_die_creation(creator, benchmark):
	res = benchmark(creator)
	assert list(res.keys()) == list(range(1, NUMBER_FACES + 1))


def matmult():
	return 50 @ ds.d(50)


def test_matmult(benchmark):
	res = benchmark(matmult)
	assert (
		res._units
		== 8881784197001252323389053344726562500000000000000000000000000000000000000000000000000  # noqa: E501
	)

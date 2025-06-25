import pytest
from groups import group_die_creation
from macros import CREATION_FACES

import dicechanics as ds


def die_from_number():
	return ds.d(CREATION_FACES)


def die_from_iterable():
	return ds.d(range(1, CREATION_FACES + 1))


def die_from_text():
	return ds.d(f"1..{CREATION_FACES}")


@group_die_creation
@pytest.mark.parametrize(
	"creator", [die_from_number, die_from_iterable, die_from_text]
)
def bm_die_creation(creator, benchmark):
	res = benchmark(creator)
	assert list(res.keys()) == list(range(1, CREATION_FACES + 1))

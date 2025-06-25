import pytest


def group_ops(func):
	return pytest.mark.benchmark(group="ops")(func)


def group_multiple_dice(func):
	return pytest.mark.benchmark(group="Multiple dice")(func)


def group_die_features(func):
	return pytest.mark.benchmark(group="Die featrues")(func)


def group_die_creation(func):
	return pytest.mark.benchmark(group="Die Creation")(func)

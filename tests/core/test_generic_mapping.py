import pytest

from ttstatistics.core.groupcount import VariableCount
from ttstatistics.core.mapping import GenericMapping, expand


def test_IsEmptyOnEmptyInit():
	assert not GenericMapping()


def test_NotEmptyInit(referenceStatisticalDict):
	assert GenericMapping(referenceStatisticalDict)


def compareFloat(value, ref):
	assert abs(value - ref) < 1e-15


def CompareKeys(res, ref):
	for key, ref in zip(res.keys(), ref.keys()):
		assert key == ref


def CompareValues(res, ref):
	for value, refvalue in zip(res.values(), ref.values()):
		compareFloat(value, refvalue)


def CompareItems(res, ref):
	for (key, value), (ref, refvalue) in zip(res.items(), ref.items()):
		assert key == ref
		compareFloat(value, refvalue)


@pytest.mark.parametrize(
	"itemsinterfaces", [CompareItems, CompareKeys, CompareValues]
)
def test_MappingInterface(itemsinterfaces, referenceStatisticalDict):
	itemsinterfaces(
		GenericMapping(referenceStatisticalDict), referenceStatisticalDict
	)


def test_Expand(FlatMapping3, FlatMapping4):
	ref = {1: 7 / 24, 2: 7 / 24, 3: 7 / 24, 4: 3 / 24}
	res = expand(GenericMapping({FlatMapping4: 1 / 2, FlatMapping3: 1 / 2}))
	CompareItems(ref, res)


""" TODO
def test_ExpandWithEmpty():
	m4 = GenericMapping({1: 1 / 4, 2: 1 / 4, 3: 1 / 4, 4: 1 / 4})
	m3 = GenericMapping({VariableCount(m4): 0, 1: 1 / 3, 2: 1 / 3, 3: 1 / 3})
	res = expand(GenericMapping({m3: 1}))
	CompareItems(res, m3)


def test_ExpandWithEmptyMutliple():
	m4 = GenericMapping({1: 1 / 4, 2: 1 / 4, 3: 1 / 4, 4: 1 / 4})
	m3 = GenericMapping({VariableCount(m4): 0, 1: 1 / 3, 2: 1 / 3, 3: 1 / 3})
	res = expand(GenericMapping({m3: 1 / 2, m4: 1 / 2}))
	ref = {VariableCount(m4): 0, 1: 7 / 24, 2: 7 / 24, 3: 7 / 24, 4: 3 / 24}
	CompareItems(res, ref)
"""

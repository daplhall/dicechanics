import pytest

from ttstatistics.core import protocols


def test_EmptyGroupIsEmpty(emptyGroup):
	assert not emptyGroup


def test_GroupNotEmpty(groupWithItems):
	assert groupWithItems


def test_prepareIsCorrectFormat(groupWithFourItems):
	for element, count in groupWithFourItems.prepare():
		assert isinstance(element, protocols.Mapping)
		assert isinstance(count, int)


def test_GetItemReturnsACopyWithSlicingStart(groupWithFourItems):
	q = groupWithFourItems[3:]
	refslice = q.prepareSlice()
	assert groupWithFourItems.items() == q.items()
	assert not refslice.next()
	assert not refslice.next()
	assert not refslice.next()
	assert refslice.next()


def test_GetItemReturnsACopySlicingInt(groupWithFourItems):
	with pytest.raises(TypeError):
		groupWithFourItems[2]


def test_bagGetItemReturnsACopySlicingArray(groupWithFourItems):
	q = groupWithFourItems[True, True, False, True]
	refslice = q.prepareSlice()
	assert groupWithFourItems.items() == q.items()
	assert refslice.next()
	assert refslice.next()
	assert not refslice.next()
	assert refslice.next()

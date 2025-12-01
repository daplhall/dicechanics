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
	assert not refslice.next()
	assert not refslice.next()
	assert not refslice.next()
	assert refslice.next()


def test_GetItemReturnsACopySlicingInt(groupWithFourItems):
	slice_ = groupWithFourItems[2].prepareSlice()
	assert not slice_.next()
	assert not slice_.next()
	assert slice_.next()
	assert not slice_.next()


def test_bagGetItemReturnsACopySlicingArray(groupWithFourItems):
	q = groupWithFourItems[0, 1, -1]
	refslice = q.prepareSlice()
	assert refslice.next()
	assert refslice.next()
	assert not refslice.next()
	assert refslice.next()


def test_GroupSliceBitwiseAnd(groupWithFourItems):
	q = (0, 1, 3) & groupWithFourItems
	refslice = q.prepareSlice()
	assert refslice.next()
	assert refslice.next()
	assert not refslice.next()
	assert refslice.next()


def test_GroupSliceBitwiseAndList(groupWithFourItems):
	q = [0, 1, 3] & groupWithFourItems
	refslice = q.prepareSlice()
	assert refslice.next()
	assert refslice.next()
	assert not refslice.next()
	assert refslice.next()


def test_GroupSliceBitwiseXOR(groupWithFourItems):
	q = (0, 1, 3) ^ groupWithFourItems
	refslice = q.prepareSlice()
	assert not refslice.next()
	assert not refslice.next()
	assert refslice.next()
	assert not refslice.next()


def test_GroupSliceBitwiseXORList(groupWithFourItems):
	q = [0, 1, 3] ^ groupWithFourItems
	refslice = q.prepareSlice()
	assert not refslice.next()
	assert not refslice.next()
	assert refslice.next()
	assert not refslice.next()


def test_SlicePoolOutOfBounds(groupWithFourItems):
	try:
		groupWithFourItems[0, 40]
	except Exception:
		pytest.fail("An exception was raised when it shouldn't")


def test_SlicePoolOutOfBoundsNeg(groupWithFourItems):
	try:
		groupWithFourItems[0, -40]
	except Exception as e:
		pytest.fail(f"An exception was raised when it shouldn't: {e}")

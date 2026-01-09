import pytest

from ttstatistics.core import protocols
from ttstatistics.core.group import Group


def test_EmptyGroupIsEmpty():
	assert not Group()


def test_GroupNotEmpty(groupWithItems):
	assert groupWithItems


def test_prepareIsCorrectFormat(Group4Items):
	for element, count in Group4Items.prepare():
		assert isinstance(element, protocols.Mapping)
		assert isinstance(count, int)


def test_SliceNormal(Group4Items):
	q = Group4Items[3:]
	refslice = q.prepareSlice()
	assert not refslice.next()
	assert not refslice.next()
	assert not refslice.next()
	assert refslice.next()


def test_SliceInteger(Group4Items):
	slice_ = Group4Items[2].prepareSlice()
	assert not slice_.next()
	assert not slice_.next()
	assert slice_.next()
	assert not slice_.next()


def getItem(mapping):
	return mapping[0, 1, -1]


def bitAndTuple(mapping):
	return (0, 1, 3) & mapping


def bitAndList(mapping):
	return [0, 1, 3] & mapping


@pytest.mark.parametrize("operation", [getItem, bitAndList, bitAndTuple])
def test_SliceAND(Group4Items, operation):
	pool = operation(Group4Items)
	slice = pool.prepareSlice()
	assert slice.next()
	assert slice.next()
	assert not slice.next()
	assert slice.next()


def bitOrList(mapping):
	return [0, 1, 3] ^ mapping


def bitOrTuble(mapping):
	return (0, 1, 3) ^ mapping


@pytest.mark.parametrize("operation", [bitOrList, bitOrTuble])
def test_SliceXOR(Group4Items, operation):
	pool = operation(Group4Items)
	slice = pool.prepareSlice()
	assert not slice.next()
	assert not slice.next()
	assert slice.next()
	assert not slice.next()


def upperBound(mapping):
	return mapping[0, 40]


def lowerBound(mapping):
	return mapping[0, -40]


@pytest.mark.parametrize("operation", [upperBound, lowerBound])
def test_SliceOutOfBounds(Group4Items, operation):
	try:
		operation(Group4Items)
	except Exception as e:
		pytest.fail(f"An exception was raised when it shouldn't: {e}")

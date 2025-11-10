import pytest

from ttstatistics.core import protocols


def test_emptyBagIsEmpty(emptyBag):
	assert not emptyBag


def test_bagNotEmpty(bagWithItems):
	assert bagWithItems


def test_prepareIsCorrectFormat(bagWithFourItems):
	for element, count in bagWithFourItems.prepare():
		assert isinstance(element, protocols.Mapping)
		assert isinstance(count, int)


def test_bagGetItemReturnsACopyWithSlicingStart(bagWithFourItems):
	q = bagWithFourItems[3:]
	refslice = q.prepareSlice()
	assert bagWithFourItems.items() == q.items()
	assert not refslice.next()
	assert not refslice.next()
	assert not refslice.next()
	assert refslice.next()


def test_bagGetItemReturnsACopySlicingInt(bagWithFourItems):
	with pytest.raises(TypeError):
		bagWithFourItems[2]


def test_bagGetItemReturnsACopySlicingArray(bagWithFourItems):
	q = bagWithFourItems[True, True, False, True]
	refslice = q.prepareSlice()
	assert bagWithFourItems.items() == q.items()
	assert refslice.next()
	assert refslice.next()
	assert not refslice.next()
	assert refslice.next()

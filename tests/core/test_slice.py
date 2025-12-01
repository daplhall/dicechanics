from ttstatistics.core.slice import Slice


def test_SliceIsEmptyOnEmptyInit(emptySlice):
	assert not emptySlice


def test_SliceIsNotEmptyOnInitSlice():
	notEmptySlice = Slice.fromSlice(slice(3))
	assert notEmptySlice


def test_SliceIsNotEmptyOnInitFromList():
	notEmptySlice = Slice.fromList([True])
	assert notEmptySlice


def test_SliceShiftToNextFromBitMask():
	notEmptySlice = Slice.fromList([True, False, True, False])
	assert notEmptySlice.next()
	assert not notEmptySlice.next()
	assert notEmptySlice.next()
	assert not notEmptySlice.next()


def test_SliceShiftToNextToMuch():
	notEmptySlice = Slice.fromList([True, False, True, False])
	assert notEmptySlice.next()
	assert not notEmptySlice.next()
	assert notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()


def test_SliceShiftToNextFromSliceStart():
	notEmptySlice = Slice.fromSlice(slice(3, None, None))
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert notEmptySlice.next()
	assert notEmptySlice.next()


def test_SliceShiftToNextFromSliceStop():
	notEmptySlice = Slice.fromSlice(slice(None, 3, None))
	assert notEmptySlice.next()
	assert notEmptySlice.next()
	assert notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()


def test_SliceShiftToNextFromSliceStep():
	notEmptySlice = Slice.fromSlice(slice(None, None, 2))
	assert notEmptySlice.next()
	assert not notEmptySlice.next()
	assert notEmptySlice.next()
	assert not notEmptySlice.next()
	assert notEmptySlice.next()
	assert not notEmptySlice.next()


def test_SliceShiftToNextFromSliceStartAndStep():
	notEmptySlice = Slice.fromSlice(slice(3, None, 4))
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert notEmptySlice.next()


def test_SliceShiftToNextFromSliceStopAndStep():
	notEmptySlice = Slice.fromSlice(slice(None, 7, 4))
	assert notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()


def test_SliceShiftToNextFromSliceAll():
	notEmptySlice = Slice.fromSlice(slice(2, 7, 4))
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()


def test_SliceShiftToNextFromSliceNegativeStart():
	notEmptySlice = Slice.fromSlice(slice(-1, 3, 2))
	assert notEmptySlice.next()
	assert not notEmptySlice.next()
	assert notEmptySlice.next()
	assert not notEmptySlice.next()


def test_SliceShiftPrevious():
	notEmptySlice = Slice.fromSlice(slice(-1, 3, 2))
	a = notEmptySlice.next()
	notEmptySlice.next()
	assert a == notEmptySlice.previous()


def test_SliceShiftReturnToOrigin():
	notEmptySlice = Slice.fromSlice(slice(None, 10, 2))
	ref = None
	for _ in range(10):
		q = notEmptySlice.next()
		if ref is None:
			ref = q
	for _ in range(10):
		notEmptySlice.previous()
	assert notEmptySlice.next() == ref


def test_SliceShiftToNextFromSliceNegativeStep():
	notEmptySlice = Slice.fromSlice(slice(3, None, -1))
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert not notEmptySlice.next()
	assert notEmptySlice.next()
	assert notEmptySlice.next()

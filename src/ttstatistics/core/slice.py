__all__ = ["Slice"]

from collections.abc import Sized


class Slice:
	def __init__(self):
		self.sliceData: slice = None
		self.listData = []
		self.cursor = -1
		self.shiftFunction = lambda: None

	def __bool__(self):
		if self.sliceData:
			return bool(self.sliceData)
		else:
			return bool(self.listData)

	def _shiftSliceBased(self) -> bool:
		start = self.sliceData.start
		if start is None:
			start = 0
		stop: int | None = self.sliceData.stop
		step = 1 if self.sliceData.step is None else self.sliceData.step
		if self.cursor < start:
			return False
		elif stop is not None and self.cursor >= stop:
			return False
		elif (self.cursor - max(start, 0)) % step != 0:
			return False
		else:
			return True

	def _shiftListBased(self) -> bool:
		return (
			self.listData[self.cursor]
			if self.cursor < len(self.listData)
			else False
		)

	@classmethod
	def fromSlice(cls, slicing: slice):
		self = cls()
		self.sliceData = slicing
		self.shiftFunction = self._shiftSliceBased
		return self

	@classmethod
	def fromList(cls, listing):
		self = cls()
		self.listData = listing
		self.shiftFunction = self._shiftListBased
		return self

	def next(self) -> bool:
		self.cursor += 1
		return self.shiftFunction()

	def previous(self) -> bool:
		self.cursor -= 1
		return self.shiftFunction()

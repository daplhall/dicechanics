__all__ = ["Slice"]


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

	def copy(self):
		out = type(self)()
		out.sliceData = self.sliceData
		out.listData = self.listData
		out.cursor = self.cursor
		out.shiftFunction = self.shiftFunction
		return out

	@staticmethod
	def _shiftSliceBased(slice_) -> bool:
		start = slice_.sliceData.start
		if start is None:
			start = 0
		stop: int | None = slice_.sliceData.stop
		step = 1 if slice_.sliceData.step is None else slice_.sliceData.step
		if slice_.cursor < start:
			return False
		elif stop is not None and slice_.cursor >= stop:
			return False
		elif (slice_.cursor - max(start, 0)) % step != 0:
			return False
		else:
			return True

	@staticmethod
	def _shiftListBased(slice_) -> bool:
		return (
			slice_.listData[slice_.cursor]
			if slice_.cursor < len(slice_.listData)
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
		return self.shiftFunction(self)

	def previous(self) -> bool:
		self.cursor -= 1
		return self.shiftFunction(self)

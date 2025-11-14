class Slice:
	def __init__(self):
		self.data = []
		self.cursor = -1
		self.shiftFunction = None

	def __bool__(self):
		return bool(self.data)

	def __hash__(self):
		return hash((self.data, self.cursor))

	def setData(self, data):
		self.data = data

	def _shiftSliceBased(self):
		start = 0 if self.data.start is None else self.data.start
		stop = self.data.stop
		step = 1 if self.data.step is None else self.data.step
		if self.cursor < start:
			return False
		elif stop is not None and self.cursor >= stop:
			return False
		elif (self.cursor - max(start, 0)) % step != 0:
			return False
		else:
			return True

	def _shiftListBased(self):
		return self.data[self.cursor] if self.cursor < len(self.data) else False

	def nextFromSlice(self):
		self.cursor += 1
		return self._shiftSliceBased()

	def nextFromList(self):
		self.cursor += 1
		return self._shiftListBased()

	@classmethod
	def fromSlice(cls, slicing):
		self = cls()
		self.setData(slicing)
		self.shiftFunction = self._shiftSliceBased
		return self

	@classmethod
	def fromList(cls, listing):
		self = cls()
		self.setData(listing)
		self.shiftFunction = self._shiftListBased
		return self

	def next(self):
		self.cursor += 1
		return self.shiftFunction()

	def previous(self):
		self.cursor -= 1
		return self.shiftFunction()

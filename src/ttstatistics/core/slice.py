class Slice:
	def __init__(self):
		self.data = []
		self.cursor = -1
		self.nextFrom = None

	def __bool__(self):
		return bool(self.data)

	def setData(self, data):
		self.data = data

	def nextFromSlice(self):
		self.cursor += 1
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

	def nextFromList(self):
		self.cursor += 1
		out = self.data[self.cursor] if self.cursor < len(self.data) else False
		return out

	@classmethod
	def fromSlice(cls, slicing):
		self = cls()
		self.setData(slicing)
		self.nextFrom = self.nextFromSlice
		return self

	@classmethod
	def fromList(cls, listing):
		self = cls()
		self.setData(listing)
		self.nextFrom = self.nextFromList
		return self

	def next(self):
		return self.nextFrom()

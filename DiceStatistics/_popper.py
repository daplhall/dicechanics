
class DicePopper(object):
	faces: list[int|float]
	count: list[int]
	def __init__(self, dice):
		data = dice._data
		self.faces = tuple(data.keys())
		self.count = tuple(data.values())
		self.i = len(self.faces)-1
	
	def identifier(self):
		return tuple(self.faces) + tuple(self.count) + (self.i,)

	def max(self):
		if self.i < 0:
			return None
		return self.faces[self.i]

	def pop(self):
		"""
			i need to do that i is -1 when the last element is popped.
			now i == 0 even if the last count is 0	
		"""
		if self.i < 0:
			return None
		face = self.faces[self.i]	
		self.count[self.i] -= 1
		if self.count[self.i] == 0:
			self.i -= 1
		return face

	def copy(self):
		res = DicePopper.__new__(DicePopper)
		res.faces = self.faces
		res.count = self.count.copy()
		res.i = self.i
		return res

	def __bool__(self):
		return self.i > -1
	
	def __str__(self):
		return f"i: {self.i} - " + str(tuple(zip(self.faces, self.count)))

	def __repr__(self):
		return str(self)
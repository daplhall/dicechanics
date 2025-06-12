
from dicechanics._Die import convert_to_dice

class DicePopper(object):
	faces: list[object]
	count: list[int]
	def __init__(self, dice):
		dice = convert_to_dice(dice)
		data = dice._data
		self.faces = list(data.keys())
		self.count = list(data.values())
		self.i = len(self.faces)-1
		self.c = self.count[self.i]
	
	def identifier(self):
		"""
		When i updated this i got quite a performance increase!	
		"""
		return tuple(self.faces) + (self.i, self.c)

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
		count = self.count[self.i]
		self.i -= 1
		return face, count

	def copy(self):
		res = DicePopper.__new__(DicePopper)
		res.faces = self.faces
		res.count = self.count
		res.i = self.i
		res.c = self.c
		return res

	def __bool__(self):
		return self.i > -1
	
	def __str__(self):
		return f"i: {self.i} - " + str(tuple(zip(self.faces, self.count)))

	def __repr__(self):
		return str(self)
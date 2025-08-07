from dicechanics.Die import Die, convert_to_die

type DicePopper_T = DicePopper


class DicePopper:
	"""
	Class responsible for "popping" the highest value data of a die
	Used in _dice_combinatorics
	"""

	faces: list[object]
	count: list[int]

	def __init__(self, dice: Die):
		dice = convert_to_die(dice)
		data = dice._data
		self.faces = list(data.keys())
		self.count = list(data.values())
		self.i = len(self.faces) - 1
		self._basehash = tuple(self.faces)

	def identifier(self) -> tuple:
		"""
		Returns a hashable object to identify the popper object

		Returns
		-------
		out: tuple
			tuple that can be hashed to identify the object
		"""
		return self._basehash + (self.i,)

	def max(self) -> object:
		"""
		Returns the highest value of the dice.

		Returns
		-------
		out: object
			Max value of the dice, None if no more values are left
		"""
		if self.i < 0:
			return None
		return self.faces[self.i]

	def pop(self) -> object:
		"""
		Pops the max value of the dice

		Returns
		-------
		out: object
			The max of the dice
		"""
		if self.i < 0:
			return None
		face = self.faces[self.i]
		count = self.count[self.i]
		self.i -= 1
		return face, count

	def copy(self) -> DicePopper_T:
		"""
		Copies the current object

		Returns
		-------
		out: DicePopper
			Copy of the current object
		"""
		res = DicePopper.__new__(DicePopper)
		res.faces = self.faces
		res.count = self.count
		res.i = self.i
		res._basehash = self._basehash
		return res

	def __bool__(self):
		return self.i > -1

	def __str__(self):
		return repr(self)  # pragma: no cover

	def __repr__(self):
		return f"i: {self.i} - " + str(
			tuple(zip(self.faces[: self.i], self.count[: self.i]))
		)  # pragma: no cover

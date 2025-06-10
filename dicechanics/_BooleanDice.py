import dicechanics as ds

class BooleanDice(ds.Dice):
	def __init__(self, faces, truth: bool):
		super().__init__(faces)
		self._truth = truth
		
	@classmethod
	def from_dice(cls, dice:ds.Dice, truth: bool):
		self = cls.from_dict(dice._data)
		self._truth = truth
		return self
		
	def __bool__(self):
		return self._truth
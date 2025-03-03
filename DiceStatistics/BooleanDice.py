import DiceStatistics as ds

class BooleanDice(ds.Dice):
	def __init__(self, faces, truth: bool):
		super().__init__(faces)
		self._truth = truth
		
	def __bool__(self):
		return self._truth
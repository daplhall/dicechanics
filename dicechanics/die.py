from dicechanics.baseunits.dieunit import DieUnit
from dicechanics.plot import StringPlot


class Die(DieUnit):
	"""
	The class that represents a statistical presentation of a die.
	"""

	def __str__(self):
		res = (
			f"Die with mu - {self.mean:.2f}, sigma - {self.std:.2f},"
			f" faces - {len(self.outcomes)}\n"
		)  # noqa: E501h
		res += "-" * (len(res) - 1) + "\n"
		return res + StringPlot.bars(
			self.f, self.c, txt=[f"{i * 100:.2f}%" for i in self.p]
		)

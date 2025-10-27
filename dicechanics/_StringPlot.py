from numbers import Number
from typing import Any

ROUND = round
LINE_STYLE = "#"


class StringPlot:
	@staticmethod
	def entry_height(y: list[Number], max_width: int) -> list[int]:
		"""
		Calculates the height of the bars plot

		Parameters
		----------
		y : list[Number]
			a list of y-values you want to bar plot

		max_width : int
			The max width of the bars columns

		Returns
		-------
		out: list[int]
			A list of the widths for corresponding y
		"""
		mx = max(y)
		width = [ROUND(i / mx * max_width) for i in y]
		return width

	@staticmethod
	def bars(
		x: list[Any],
		y: list[Number],
		txt: list[str] | None = None,
		max_width: int = 20,
	) -> str:
		"""
		Function that creates a string representation of the Die as a bar graph.

		Parameters
		----------
		x : list[Any]
			Values for the x-axis
		y : list[Numbers]
			Values for the y-axis, corresponds to x
		bars_txt: list[str]
			corresponding text for the top of the bars
			(default) None
		max_width : int
			The max width of the bars columns
			(default) 20

		Returns
		-------
		out: str
			The str with the ascii plot.
		"""
		assert len(x) == len(y)
		if txt is None:
			txt = [""] * len(x)
		res = ""
		pad = max(len(str(i)) for i in x)
		widths = StringPlot.entry_height(y, max_width)
		for key, top, w in zip(x, txt, widths):
			res += f"{key:>{pad}}" + "|" + LINE_STYLE * w + f" {top}" + "\n"
		return res

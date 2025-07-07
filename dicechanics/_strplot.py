import math

from dicechanics import Die

MAX_WIDTH = 20
ROUND = round
LINE_STYLE = "#"


def mag(x: float) -> int:
	"""
	Calculates the order of magnitude of a given number.

	Parameters
	----------
	x : float
		the value which the order of magnitude needs to be found.

	Returns
	-------
	out: int
		The order of magnitude.
	"""
	return int(math.log10(x))


def calc_width(data: Die) -> list[int]:
	"""
	Calculates the width/height of the plot values normalized to the macro
	MAX_WIDTH.

	Parameters
	----------
	data: Die
		The Die whose width needs to be found.

	Returns
	-------
	out: list[int]
		A list of the widths corresponding to the dies faces.
	"""
	mx = max(data.values())
	width = [ROUND(i / mx * MAX_WIDTH) for i in data.values()]
	return width


def str_plot(data: Die) -> str:
	"""
	Function that creates a string representation of the Die as a bar graph.

	Parameters
	----------
	data: Die
		The die that needs to be plotted

	Returns
	-------
	out: str
		The str with the ascii plot.
	"""
	res = ""
	pad = 1 + max(mag(i) for i in data.keys())
	widths = calc_width(data)
	for f, p, w in zip(data.f, data.p, widths):
		res += f"{f:>{pad}}" + "|" + LINE_STYLE * w + f" {p*100:.2f}%" + "\n"
	return res

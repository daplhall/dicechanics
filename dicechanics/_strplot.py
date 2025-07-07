import math

from dicechanics import Die

ROUND = round
LINE_STYLE = "#"


def num_len(x: float) -> int:
	"""
	Calculates how many characters a number needs to be written to screen

	Parameters
	----------
	x : float
		the value which the length needs to be found

	Returns
	-------
	out: int
		The order of magnitude.
	"""
	extra = 0
	if x == 0:
		return 1
	elif x < 0:
		x *= -1
		extra += 1
	return int(math.log10(x)) + extra


def calc_width(data: Die, max_width) -> list[int]:
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
	width = [ROUND(i / mx * max_width) for i in data.values()]
	return width


def str_plot(data: Die, max_width) -> str:
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
	pad = 1 + max(num_len(i) for i in data.keys())
	widths = calc_width(data, max_width)
	for f, p, w in zip(data.f, data.p, widths):
		res += f"{f:>{pad}}" + "|" + LINE_STYLE * w + f" {p*100:.2f}%" + "\n"
	return res

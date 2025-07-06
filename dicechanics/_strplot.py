import math

from dicechanics import Die

MAX_WIDTH = 20
FLOOR = int


def mag(x: float) -> int:
	return int(math.log10(x))


def calc_width(data: dict[object]) -> list[int]:
	mx = max(data.values())
	width = [FLOOR(i / mx * MAX_WIDTH) for i in data.values()]
	return width


def str_plot(data: Die) -> str:
	res = ""
	pad = 1 + max(mag(i) for i in data.keys())
	widths = calc_width(data)
	for f, p, w in zip(data.f, data.p, widths):
		res += f"{f:<{pad}}" + "|" + "#" * w + f" {p:.2f}" + "\n"
	return res

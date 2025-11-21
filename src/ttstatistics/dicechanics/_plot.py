class StringPlotter:
	@staticmethod
	def plot(x, y, lineHeight, style, topText):
		assert len(x) == len(y)
		if topText is None:
			topText = [""] * len(x)
		res = ""
		pad = max(len(str(i)) for i in x)
		mx = max(y)
		height = [round(i / mx * lineHeight) for i in y]
		for key, text, w in zip(x, topText, height):
			res += f"{key:>{pad}}" + "|" + style * w + f" {text}" + "\n"
		return res

	@staticmethod
	def bars(x, y, topText=""):
		return StringPlotter.plot(
			x, y, lineHeight=20, style="#", topText=topText
		)

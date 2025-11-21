class StringPlot:
	@staticmethod
	def plot(x, y, lineHeight, style, topText):
		assert len(x) == len(y)
		if topText is None:
			topText = [""] * len(x)
		assert len(topText) == len(x)
		res = ""
		pad = max(len(str(i)) for i in x)
		mx = max(y)
		height = [round(i / mx * lineHeight) for i in y]
		for key, text, w in zip(x, topText, height):
			res += f"{key:>{pad}}" + "|" + style * w + f" {text}" + "\n"
		return res

	@staticmethod
	def bars(x, y, topText=None):
		if topText is None:
			topText = y
		return StringPlot.plot(x, y, lineHeight=20, style="#", topText=topText)

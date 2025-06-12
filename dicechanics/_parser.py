from dicechanics.typing import NumVector


def text_to_faces(text: str) -> NumVector:
	if (
		any(c.isalpha() for c in text) or ";" in text
	):  # the alpha check out be ommited.
		raise Exception("illegal charaters in dice parsing")

	out: NumVector = []

	f = text.split(",")
	for strf in f:
		if ".." in strf and ":" in strf:
			if strf.index("..") > strf.index(":"):
				raise Exception("':' comes before '..'")
			strf = strf.replace(":", ",")
			strf = strf.replace("..", ",")
			c = strf.split(",")
			for i in range(int(c[2])):
				for i in range(int(c[0]), int(c[1]) + 1):
					out.append(i)
		elif ".." in strf:
			c = strf.split("..")
			# TODO maybe we need some linspacing here if we have floating point numbers.  # noqa: E501
			for i in range(int(c[0]), int(c[1]) + 1):
				out.append(i)
		elif ":" in strf:
			c = strf.split(":")
			for i in range(int(c[1])):
				out.append(float(c[0]) if "." in c[0] else int(c[0]))
		else:
			out.append(float(strf) if "." in strf else int(strf))
	return out

def unique(array):
	w = []
	c = []
	for v in array:
		if v not in w:
			w.append(v)
			c.append(1)
		else:
			i = w.index(v)
			c[i] += 1
	return w,c

def dice_parse(text:str) -> list:
	res = []
	f = text.split(',')
	for strf in f:
		if ".." in strf and ':' in strf :
			if strf.index("..") > strf.index(':'):
				raise Exception("':' comes before '..'")
			strf = strf.replace(':', ',')
			strf = strf.replace('..', ',')
			c = strf.split(',')
			for i in range(int(c[2])):
				for i in range(int(c[0]),int(c[1]) + 1):
					res.append(i)
		elif ".." in strf:
			c = strf.split('..')
			# TODO maybe we need some linspacing here if we have floating point numbers.
			for i in range(int(c[0]),int(c[1]) + 1):
				res.append(i)
		elif ":" in strf:
			c = strf.split(':')
			for i in range(int(c[1])):
				res.append(float(c[0]) if '.' in c[0] 
							else int(c[0]))
		else:
			res.append(float(strf) if '.' in strf else int(strf))
	return res

def parse_to_prop(text:str):
	"""
	returns the count and properbility written in the string sequence of text
	"""
	if  any(c.isalpha() for c in text) or ';' in text: # the alpha check out be ommited.
		raise Exception("illegal charaters in dice parsing")
	raw_faces = dice_parse(text)
	raw_faces.sort()
	f, c = unique(raw_faces)	
	p = [i/sum(c) for i in c]
	return f, p, c
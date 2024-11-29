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
	a = []
	f = text.split(',')
	for s in f:
		if ".." in s and ':' in s :
			if s.index("..") > s.index(':'):
				raise Exception("':' comes before '..'")
			s = s.replace(':', ',')
			s = s.replace('..', ',')
			c = s.split(',')
			for i in range(int(c[2])):
				for i in range(int(c[0]),int(c[1]) + 1):
					a.append(i)
		elif ".." in s:
			c = s.split('..')
			# TODO maybe we need some linspacing here if we have floating point numbers.
			for i in range(int(c[0]),int(c[1]) + 1):
				a.append(i)
		elif ":" in s:
			c = s.split(':')
			for i in range(int(c[1])):
				a.append(float(c[0]) if '.' in c[0] 
	     						else int(c[0]))
		else:
			a.append(float(s) if '.' in s else int(s))
	return a

def parse_to_prop(text:str):
	"""
	returns the count and properbility written in the string sequence of text
	"""
	if  any(c.isalpha() for c in text) or ';' in text:
		raise Exception("illegal charaters in dice parsing")
	a = dice_parse(text)
	a.sort()
	u, c = unique(a)	
	p = [i/sum(c) for i in c]
	return u, p
import typing
from DiceStatistics._math import unique

def faces_to_count(faces: list) -> list|list|list :
	f, c = unique(faces)	
	# TODO run faces parser 
	return dict(sorted(zip(f, c), key=lambda pair: pair[0]))

def text_to_faces(text:str) -> list:
	if  any(c.isalpha() for c in text) or ';' in text: # the alpha check out be ommited.
		raise Exception("illegal charaters in dice parsing")

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
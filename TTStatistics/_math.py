
def unique(array:list) -> tuple[list,list]:
	u = []
	c = []
	for e in array:
		if e not in u:
			u.append(e)
			c.append(1)
		else:
			i = u.index(e)
			c[i] += 1
	return u,c
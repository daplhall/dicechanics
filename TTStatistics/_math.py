import math

ceil = math.ceil
floor = math.floor

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

def ceildiv(lhs: int | float, rhs: int | float):
	return -(lhs//-rhs)

def GCD(a: int, b: int) -> int:
	"""
	Greatest commen demoninator
	"""
	while b != 0:
		r = a%b
		a,b = b, r
	return a
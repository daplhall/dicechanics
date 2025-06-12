from collections.abc import Iterable
from dicechanics._Die import Die
from dicechanics._Pool import Pool
from dicechanics._parser import text_to_faces

def d(inpt:Iterable | int, **kwards) -> Die:
	if isinstance(inpt, int):
		return Die(range(1,inpt+1),**kwards)
	elif isinstance(inpt, str):
		faces = text_to_faces(inpt)
		return Die(faces, **kwards)
	elif isinstance(inpt, Iterable) :
		return Die(inpt, **kwards)
	else:
		raise Exception("Dice doens't support input type of %s"%(type(inpt)))

def z(inpt: int, **kwards) -> Die:
	return Die(range(0, inpt + 1), **kwards)

def pool(inpt:list) -> Pool:
	return Pool(inpt)
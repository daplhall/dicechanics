from collections import defaultdict

def combs_arrays(inpt: list[list], i:int , func: callable, mem: dict):
	if i in mem:
		return mem[i]
	if not inpt:
		return {}
	cur = inpt.pop()
	res = defaultdict(int)
	for f,c in cur.items():
		sub = combs_arrays(inpt.copy(), i+1, func, mem)
		if sub:
			for sf,sc in sub.items():
				res[func(f,sf)] += c*sc
		else:
			res[f] = c
	mem[i] = res
	return res
import time
from itertools import product
a = {1:5,3:2,2:1}

inpt = [a]*2
mem = {}
t = time.time()
res = combs_arrays(inpt, 0, lambda x,y: x+y, mem)
print(time.time() - t)
print(dict(res))

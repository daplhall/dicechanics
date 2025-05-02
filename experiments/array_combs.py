from collections import defaultdict

def combs_arrays(inpt: list[list], i:int , func: callable, mem: dict):
	if i in mem:
		return mem[i]
	if i >= len(inpt):
		return {}
	res = defaultdict(int)
	for f,c in inpt[i].items():
		if sub := combs_arrays(inpt, i+1, func, mem):
			for sf,sc in sub.items():
				res[func(f,sf)] += c*sc
		else:
			res[f] = c
	mem[i] = res
	return res
import time
from itertools import product
a = {f:1 for f in range(1,7)}

inpt = [a]*2
mem = {}
t = time.time()
res = combs_arrays(inpt, 0, lambda x,y: x+y, mem)
print(time.time() - t)
print(res)

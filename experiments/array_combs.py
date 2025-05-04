from collections import defaultdict

hits = 0
calls = 0
def combs_arrays(inpt: list[list], i:int , func: callable, mem: dict):
	global calls
	calls += 1
	if i in mem:
		global hits
		hits += 1
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
a = {f:1 for f in range(1,50)}
inpt = [a]*5
mem = {}
t = time.time()
res = combs_arrays(inpt, 0, lambda x,y: x+y, mem)
print(time.time() - t)
print(calls)
print(hits)
print(hits/calls)

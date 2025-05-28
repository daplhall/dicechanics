from DiceStatistics import Dice,d6
from collections import defaultdict

hits = 0
calls = 0

def linear_combs(inpt: list[Dice], i:int , func: callable, mem: dict) -> defaultdict[int]:
	if i in mem:
		return mem[i]
	if i >= len(inpt):
		return {}
	res = defaultdict(int)
	for f,c in inpt[i].items():
		if sub := linear_combs(inpt, i+1, func, mem):
			for sf,sc in sub.items():
				res[func(f,sf)] += c*sc
		else:
			res[f] = c
	mem[i] = res
	return res



import time
from itertools import product

def func(x,y):
	if isinstance(y,int):
		return (x,y)
	return (x,) + y


f = d6*d6*d6
print(f.f)
print(f.c)
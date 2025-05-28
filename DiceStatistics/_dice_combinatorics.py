from collections import defaultdict
import DiceStatistics as ds


def linear_combs(inpt: list[ds.Dice], layer:int , func: callable, mem: dict) -> defaultdict[int]:
	if layer in mem:
		return mem[layer]
	if layer >= len(inpt):
		return {}
	res = defaultdict(int)
	for f,c in inpt[layer].items():
		if sub := linear_combs(inpt, layer+1, func, mem):
			for sf,sc in sub.items():
				res[func(f,sf)] += c*sc
		else:
			res[f] = c
	mem[layer] = res
	return res

def linear_non_selective(inpt: list[ds.Dice], func: callable) -> ds.Dice:
	mem = defaultdict(int)
	res = linear_combs(inpt, 0, func, mem)
	return ds.Dice.from_dict(res)
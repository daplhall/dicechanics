from collections import defaultdict

def combinations_mem(input, parent, idx, r,  mem):
	if (parent, idx) in mem:
		return
	if r == 0:
		return 
	if idx >= len(input):
		return 
	for i in range(idx, len(input)):
		combinations_mem(input, idx, i+1, r-1, mem)
		if mem[idx,i+1]:
			for j in mem[idx,i+1]:
				mem[parent,idx].append([input[i]]+j)
		else:
			mem[parent,idx].append([input[i]])

def combs_mem(input:list, r:int):
	res = []
	data = []	
	mem = defaultdict(list)
	combinations_mem(input, -1, 0, r, mem)
	for i in mem[-1,0]:
		if len(i) == r:
			res.append(i)
	return res
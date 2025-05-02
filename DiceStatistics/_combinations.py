from line_profiler import profile
from collections import defaultdict

@profile
def combinations_mem(inpt, idx, r,  mem):
	if (idx, r) in mem:
		return
	if r == 0:
		return 
	if idx >= len(inpt):
		return 
	for i in range(idx, len(inpt)):
		combinations_mem(inpt, i+1, r-1, mem)
		if (i+1, r-1) in mem:
			# if i can find a way to make create solution as fast as this we are good
			# if not use the for loop
			#mem[idx,r].append([inpt[i]]+mem[i+1,r-1])
			for j in mem[i+1, r-1]:
				mem[idx, r].append([input[i]]+j)
		else:
			mem[idx,r].append([inpt[i]])
		#print("", end = '')

def create_solution(inpt, res, data, r):
	if len(data) == r:
		yield data.copy()
		#return
	for i, v in enumerate(inpt):
		data.append(v[0])
		yield from create_solution(v[1:], res, data , r)
		data.pop()
		

	
def combs_mem(input:list, r:int):
	res = []
	data = []	
	mem = defaultdict(list)
	#combinations_mem(input, 0, r, mem)
	#yield from create_solution(mem[0,r], res, data, r)
	for i in mem[0,3]:
		if len(i) == r:
			res.append(i)
	return res

input = list(range(50))
r = 3
combs_mem(input, r)

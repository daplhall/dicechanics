from collections import defaultdict
from functools import cache
from math import comb

from ttstatistics.core.bag import Bag
from ttstatistics.core.genericmapping import GenericMapping
from ttstatistics.core.operations import micro


def getOutcomes(bag):
	res = defaultdict(int)
	for idx, (mapping, amount) in enumerate(bag.prepare()):
		for key, count in mapping.items():
			res[(key, idx)] += count * amount

	return sorted(res.items(), key=lambda x: x[0], reverse=True)


def BaseChosenValue(operation, face, nChosen):
	assert nChosen > 0
	base = face  # shouldnt be done if nchosen is zero
	for i in range(nChosen - 1):
		base = operation(base, face)
	return base


def writeSubToRes(res, sub):
	for face, amount in sub.items():
		res[face] += amount


def writeOutcomeToRes(res, operation, base, sub, combinations):
	if sub == {None: 1}:
		res[base] += combinations
		return
	for face, amount in sub.items():
		res[operation(face, base)] += amount * combinations


def anyLeft(outcomes):
	return not outcomes


def bottomReturnValue(leftToChose):
	return None if leftToChose else {None: 1}


def createSubMeta(meta, idx, nChosen):
	submeta = list(meta)
	submeta[idx] -= nChosen
	return tuple(submeta)


@cache
def primoridalSelective(outcomes, sliceing, operation, leftToChose, meta):
	if anyLeft(outcomes):
		return bottomReturnValue(leftToChose)
	res = defaultdict(int)
	(face, idx), amount = outcomes[0]
	for nChosen in range(0, min(amount, leftToChose, meta[idx]) + 1):
		submeta = createSubMeta(meta, idx, nChosen)
		sub = primoridalSelective(
			outcomes[1:], sliceing, operation, leftToChose - nChosen, submeta
		)
		if sub is None:
			continue
		if nChosen == 0:
			writeSubToRes(res, sub)
		else:
			base = BaseChosenValue(operation, face, nChosen)
			writeOutcomeToRes(
				res, operation, base, sub, comb(leftToChose, nChosen)
			)

	return res


# d = GenericMapping({1: 1, 2: 1})
d = GenericMapping(dict.fromkeys(range(1, 7), 1))
g = GenericMapping(dict.fromkeys(range(1, 4), 1))
N = 4
M = 0
import time

mybag = Bag({d: N, g: M})
outcomes = getOutcomes(mybag[1:])
print(outcomes)
meta = (N, M)

t = time.perf_counter()
res = primoridalSelective(
	tuple(outcomes), mybag.prepareSlice(), micro.add, N + M, meta
)
print(time.perf_counter() - t)
for k, v in res.items():
	print(k, round(v / sum(res.values()) * 100, 4))

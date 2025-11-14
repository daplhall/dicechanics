"""
Tmp for selective
"""

from collections import defaultdict
from math import comb


def getOutcomes(bag):
	res = defaultdict(int)
	for mapping, amount in bag.prepare():
		for key, count in mapping.items():
			res[key] += count * amount

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


def primoridalSelective(outcomes, operation, leftToChose):
	if not outcomes:
		if leftToChose:
			return None
		else:
			return {None: 1}
	res = defaultdict(int)
	face, amount = outcomes[0]
	for nChosen in range(0, min(amount, leftToChose) + 1):
		sub = primoridalSelective(
			outcomes[1:], operation, leftToChose - nChosen
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


"""
meta is just list of amounts for idx
if we have 5 number of idx 0
then meta[idx] = 5
"""


def primoridalSelectiveDifferentDie(outcomes, operation, leftToChose, meta):
	if not outcomes:
		if leftToChose:
			return None
		else:
			return {None: 1}
	res = defaultdict(int)
	(face, idx), amount = outcomes[0]
	for nChosen in range(0, min(amount, leftToChose, meta[idx]) + 1):
		submeta = meta.copy()
		submeta[idx] -= nChosen
		sub = primoridalSelective(
			outcomes[1:], operation, leftToChose - nChosen, submeta
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

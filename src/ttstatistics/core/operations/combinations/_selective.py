__all__ = ["Selective", "getOutcomes"]

from collections import defaultdict
from functools import cache
from math import comb


def getOutcomes(bag):
	res = defaultdict(int)
	amountTuple = ()
	for idx, (mapping, amount) in enumerate(bag.prepare()):
		for key, probability in mapping.items():
			res[(key, idx, probability)] += amount
		amountTuple += (amount,)

	return tuple(
		sorted(res.items(), key=lambda x: x[0], reverse=True)
	), amountTuple


class Selective:
	# if left to choose is higher than n chosen then we can just return None if we are at the bottom
	@cache
	def calculate(self, outcomes, operation, leftToChose, meta, slicing):
		if anyOutcomesLeft(outcomes):
			return bottomOutcome(leftToChose)
		res = defaultdict(int)
		(outcome, idx, weight), amount = outcomes[0]
		for nChosen in range(0, min(amount, leftToChose, meta[idx]) + 1):
			# loop unroling?
			subMeta = createSubMeta(meta, idx, nChosen)
			subAmount = leftToChose - nChosen
			sub = self.calculate(
				outcomes[1:], operation, subAmount, subMeta, slicing[nChosen:]
			)
			if sub is None:
				pass
			elif nChosen == 0:
				writeSubToRes(res, sub)
			else:
				baseValue = combinedOutcome(
					operation, outcome, nChosen, slicing[:nChosen]
				)
				coef = weightedBinaryCoeficients(leftToChose, nChosen, weight)
				writeOutcomeToRes(res, operation, baseValue, sub, coef)
		return res


def combinedOutcome(operation, face, nChosen, sliceMask):
	assert nChosen > 0
	base = None  # shouldnt be done if nchosen is zero
	for i, truth in zip(range(nChosen), sliceMask):
		if not truth:
			continue
		if base is None:
			base = face
		else:
			base = operation(base, face)
	return base


def writeSubToRes(res, sub):
	for face, amount in sub.items():
		res[face] += amount


def writeOutcomeToRes(res, operation, baseValue, sub, combinations):
	for face, amount in sub.items():
		if face is None:
			res[baseValue] += amount * combinations
		elif baseValue is None:
			res[face] += amount * combinations
		else:
			res[operation(face, baseValue)] += amount * combinations


def anyOutcomesLeft(outcomes):
	return not outcomes


def bottomOutcome(leftToChose):
	return None if leftToChose else {None: 1}


def createSubMeta(meta, idx, nChosen):
	submeta = list(meta)
	submeta[idx] -= nChosen
	return tuple(submeta)


def weightedBinaryCoeficients(leftToChose, nChosen, weight):
	BinaryCoeficients = comb(leftToChose, nChosen)
	return BinaryCoeficients * weight**nChosen


def crankSliceBack(slicing, nTimes):
	for i in range(nTimes):
		slicing.previous()


def crankSliceForward(slicing, nTimes) -> list[bool]:
	return [slicing.next() for i in range(nTimes)]

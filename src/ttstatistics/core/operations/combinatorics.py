from collections import defaultdict
from collections.abc import Callable
from functools import cache
from math import comb

from ttstatistics.core.protocols.base import Unit
from ttstatistics.utils.reference import Reference

type BagItems = list[tuple[Unit, int]]


def updateWithOperations(current, subproblem, operation, res):
	key, value = current
	for skey, svalue in subproblem.items():
		res[operation(key, skey)] += svalue * value


def updateNoSubproblem(current, res):
	key, value = current
	res[key] = value


def countDownAmount(items: BagItems, layer: int):
	mapping, count = items[layer]
	items[layer] = mapping, count - 1
	return mapping, count


def whoIsNext(layer: int, count: int):
	return layer + 1 if count <= 1 else layer


def isEndOfBranch(items: BagItems, layer: int):
	return layer >= len(items)


def combinations(
	items: BagItems,
	operation: Callable[[Unit, Unit], Unit],
	whom: int,
	mem: Reference,
):
	if mem:
		return mem.get()
	if isEndOfBranch(items, whom):
		return {}
	res = defaultdict(int)
	mapping, count = countDownAmount(items, whom)
	for curr in mapping.items():
		if sub := combinations(
			items,
			operation,
			whoIsNext(whom, count),
			mem,
		):
			updateWithOperations(curr, sub, operation, res)
		else:
			updateNoSubproblem(curr, res)
	mem.set(res)
	return res


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


def anyLeft(outcomes):
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


def windSliceBack(slicing, nTimes):
	for i in range(nTimes):
		slicing.previous()


def windSliceForward(slicing, nTimes) -> list[bool]:
	return [slicing.next() for i in range(nTimes)]


# if left to choose is higher than n chosen then we can just return None if we are at the bottom
@cache
def selective(outcomes, operation, leftToChose, meta, slicing):
	if anyLeft(outcomes):
		return bottomOutcome(leftToChose)
	res = defaultdict(int)
	(outcome, idx, weight), amount = outcomes[0]
	for nChosen in range(0, min(amount, leftToChose, meta[idx]) + 1):
		sliceMask = windSliceForward(slicing, nChosen)
		subMeta = createSubMeta(meta, idx, nChosen)
		subAmount = leftToChose - nChosen
		sub = selective(outcomes[1:], operation, subAmount, subMeta, slicing)
		if sub is None:
			pass
		elif nChosen == 0:
			writeSubToRes(res, sub)
		else:
			baseValue = combinedOutcome(operation, outcome, nChosen, sliceMask)
			coef = weightedBinaryCoeficients(leftToChose, nChosen, weight)
			writeOutcomeToRes(res, operation, baseValue, sub, coef)
		windSliceBack(slicing, nChosen)
	return res if res else None

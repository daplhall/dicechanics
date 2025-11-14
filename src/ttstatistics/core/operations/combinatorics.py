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


def BaseChosenValue(operation, face, nChosen, sliceMask):
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


def writeOutcomeToRes(res, operation, base, sub, combinations):
	for face, amount in sub.items():
		if face is None:
			res[base] += amount * combinations
		else:
			res[operation(face, base)] += amount * combinations


def anyLeft(outcomes):
	return not outcomes


def bottomReturnValue(leftToChose):
	return None if leftToChose else {None: 1}


def createSubMeta(meta, idx, nChosen):
	submeta = list(meta)
	submeta[idx] -= nChosen
	return tuple(submeta)


def weightedBinaryCoeficients(leftToChose, nChosen, probability):
	BinaryCoeficients = comb(leftToChose, nChosen)
	return BinaryCoeficients * probability**nChosen


# if left to choose is higher than n chosen then we can just return None if we are at the bottom
@cache
def selective(outcomes, operation, leftToChose, meta, slicing):
	if anyLeft(outcomes):
		return bottomReturnValue(leftToChose)
	res = defaultdict(int)
	(face, idx, probability), amount = outcomes[0]
	for nChosen in range(0, min(amount, leftToChose, meta[idx]) + 1):
		submeta = createSubMeta(meta, idx, nChosen)
		sliceMask = [slicing.next() for i in range(nChosen)]
		sub = selective(
			outcomes[1:], operation, leftToChose - nChosen, submeta, slicing
		)
		if sub is None:
			for i in range(nChosen):
				slicing.previous()
			continue
		if nChosen == 0:
			writeSubToRes(res, sub)
		else:
			base = BaseChosenValue(operation, face, nChosen, sliceMask)
			print(base)
			coef = weightedBinaryCoeficients(leftToChose, nChosen, probability)
			writeOutcomeToRes(res, operation, base, sub, coef)
			for i in range(nChosen):
				slicing.previous()
	return res if res else None

__all__ = ["Selective", "getOutcomes"]

from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from math import comb

from ttstatistics.core import protocols
from ttstatistics.core.empty import VariableCount
from ttstatistics.utils.utils import normalize


def getOutcomes(bag: protocols.Group):
	res = defaultdict(int)
	amountTuple = ()
	testTuple = ()
	for idx, (mapping, amount) in enumerate(bag.prepare()):
		for key, probability in mapping.items():
			res[(key, idx, probability)] += amount
		if isinstance(amount, VariableCount):
			testTuple += (((None, idx, None), amount),)
		amountTuple += (0 + amount,)  # hack needs cleaning up

	return (
		tuple(sorted(res.items(), key=lambda x: x[0])),
		amountTuple,
		testTuple,
	)


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
	if None in sub:
		assert len(sub) == 1
		res[baseValue] += sub[None] * combinations
	elif baseValue is None:
		for face, amount in sub.items():
			res[face] += amount * combinations
	else:
		for face, amount in sub.items():
			res[operation(face, baseValue)] += amount * combinations


def isOutcomesEmpty(outcomes):
	return not outcomes


def isGroupEmpty(leftToChose):
	return leftToChose == 0


def weightedBinaryCoeficients(leftToChose, nChosen, weight):
	BinaryCoeficients = comb(leftToChose, nChosen)
	return BinaryCoeficients * weight**nChosen


@dataclass(frozen=True)
class GroupCounts:
	memberCount: tuple[int]
	total: int

	def subGroup(self, idx: int, nChosen: int) -> "GroupCounts":
		subMeta = list(self.memberCount)
		subMeta[idx] -= nChosen
		return GroupCounts(tuple(subMeta), self.total - nChosen)

	def subGroupEmpty(self, n):
		return GroupCounts(self.memberCount, self.total - n)


class Selective:
	def calculate(
		self, group: protocols.Group, operation: protocols.InputFunction
	):
		outcomes, counts, slice_ = self.prepare(group)
		return normalize(self._evaluate(outcomes, operation, counts, slice_))

	def prepare(self, group: protocols.Group):
		bagSlice = group.prepareSlice()
		outcomes, meta, empty = getOutcomes(group)
		slice_ = tuple(bagSlice.next() for _ in range(sum(meta)))
		order = self.orientation(slice_)
		return (
			empty + outcomes[::order],
			GroupCounts(meta, sum(meta)),
			slice_[::order],
		)

	def orientation(self, sliceList):
		length = len(sliceList)
		upper = sum(sliceList[length // 2 :])
		lower = sum(sliceList[: length // 2])
		if upper > lower:
			return -1
		else:
			return 1

	@cache
	def _evaluate(self, outcomes, operation, counts: GroupCounts, slicing):
		if isGroupEmpty(counts.total):
			return {None: 1}
		if isOutcomesEmpty(outcomes):
			return None
		res = defaultdict(int)
		amount: float | VariableCount
		(outcome, idx, weight), amount = outcomes[0]
		if not isinstance(amount, VariableCount):
			nmax = min(amount, counts.total, counts.memberCount[idx])
			for n in range(0, nmax + 1):
				subGroup = counts.subGroup(idx, n)
				sub = self._evaluate(
					outcomes[1:], operation, subGroup, slicing[n:]
				)
				if sub is None:
					pass
				elif n == 0:
					writeSubToRes(res, sub)
				else:
					baseValue = combinedOutcome(
						operation, outcome, n, slicing[:n]
					)
					coef = weightedBinaryCoeficients(counts.total, n, weight)
					writeOutcomeToRes(res, operation, baseValue, sub, coef)
		else:
			for n, w in amount.counts.items():
				subGroup = counts.subGroup(idx, amount.max - n)
				sub = self._evaluate(outcomes[1:], operation, subGroup, slicing)
				for sf, sw in sub.items():
					res[sf] += sw * w

		return res

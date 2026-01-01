__all__ = ["Selective", "getOutcomes"]

from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from math import comb

from ttstatistics.core import protocols
from ttstatistics.utils.utils import normalize


def getOutcomes(bag: protocols.Group):
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
	if None in sub:
		assert len(sub) == 1
		res[baseValue] += sub[None] * combinations
	elif baseValue is None:
		for face, amount in sub.items():
			res[face] += amount * combinations
	else:
		for face, amount in sub.items():
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


class Selective:
	def calculate(
		self, group: protocols.Group, operation: protocols.InputFunction
	):
		bagSlice = group.prepareSlice()
		outcomes, meta = getOutcomes(group)
		slice_ = tuple(bagSlice.next() for _ in range(sum(meta)))[::-1]
		return normalize(
			self._evaluate(outcomes, operation, sum(meta), meta, slice_)
		)

	@cache
	def _evaluate(self, outcomes, operation, leftToChose, meta, slicing):
		if anyOutcomesLeft(outcomes) or leftToChose == 0:
			return bottomOutcome(leftToChose)
		res = defaultdict(int)
		(outcome, idx, weight), amount = outcomes[0]
		for nChosen in range(0, min(amount, leftToChose, meta[idx]) + 1):
			# loop unroling?
			subMeta = createSubMeta(meta, idx, nChosen)
			subAmount = leftToChose - nChosen
			sub = self._evaluate(
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


@dataclass(frozen=True)
class GroupCounts:
	memberCount: tuple[int]
	total: int


TOTAL = 0
CALLS = 0
A = 0
N0 = 0
BASE = 0
ITER = 0
from line_profiler import profile


class SelectiveCleanup:
	def calculate(
		self, group: protocols.Group, operation: protocols.InputFunction
	):
		bagSlice = group.prepareSlice()
		outcomes, meta = getOutcomes(group)
		slice_ = tuple(bagSlice.next() for _ in range(sum(meta)))[::-1]
		q = normalize(
			self._evaluate(
				outcomes, operation, GroupCounts(meta, sum(meta)), slice_
			)
		)
		print(TOTAL, CALLS, A, BASE, N0, ITER)
		return q

	@cache
	def _evaluate(self, outcomes, operation, counts: GroupCounts, slicing):
		global TOTAL, CALLS, A, BASE, N0, ITER
		CALLS += 1
		if anyOutcomesLeft(outcomes) or counts.total == 0:
			A += 1
			return bottomOutcome(counts.total)
		res = defaultdict(int)
		(outcome, idx, weight), amount = outcomes[0]
		nmax = min(amount, counts.total, counts.memberCount[idx])
		if sum(slicing) == 0:
			TOTAL += 1
		for nChosen in range(0, nmax + 1):
			ITER += 1
			subMeta = createSubMeta(counts.memberCount, idx, nChosen)
			subAmount = counts.total - nChosen
			sub = self._evaluate(
				outcomes[1:],
				operation,
				GroupCounts(subMeta, subAmount),
				slicing[nChosen:],
			)
			if sub is None:
				pass
			elif nChosen == 0:
				N0 += 1
				writeSubToRes(res, sub)
			else:
				BASE += 1
				baseValue = combinedOutcome(
					operation, outcome, nChosen, slicing[:nChosen]
				)
				coef = weightedBinaryCoeficients(counts.total, nChosen, weight)
				writeOutcomeToRes(res, operation, baseValue, sub, coef)
		return res

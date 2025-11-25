import pytest

from ttstatistics.dicechanics.symbolics import RerollSymbol


class RerollSymbolSpy(RerollSymbol):
	def inside(self):
		return self.internals

	def getDepth(self):
		return self.depth


def test_rerollCreateEmpty():
	assert not RerollSymbol()


def test_rerollCreateWithNumber():
	assert RerollSymbol(4)


def test_rerollCreateWithString():
	assert RerollSymbolSpy("a").inside() == "a"


def test_rerollAddAffectsTheObject():
	assert (RerollSymbolSpy() + 4 + 2).inside() == 6


def test_rerollSubAffectsTheObject():
	assert (RerollSymbolSpy() - 4 - 3).inside() == -7


def test_rerollMultAffectsTheObject():
	assert (RerollSymbolSpy() * 3).inside() == 3


def test_rerollDivAffectsTheObject():
	assert (RerollSymbolSpy() / 3).inside() == 3


def test_rerollFloorDivAffectsTheObject():
	assert (RerollSymbolSpy() // 3).inside() == 3


def test_rerollAddStrAffectsTheObject():
	assert (RerollSymbolSpy() + "a" + "b").inside() == "ab"


def test_rerollMixedSymbolsThrowError():
	with pytest.raises(TypeError):
		assert not ((RerollSymbol() + 4) + "a")


def test_rerollDefineDepth():
	q = RerollSymbolSpy(depth=4)
	assert q.getDepth() == 4

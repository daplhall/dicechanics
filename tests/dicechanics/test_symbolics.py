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
	assert RerollSymbol("a")


def test_rerollAddAffectsTheObject():
	assert RerollSymbol() + 4 + 2


def test_rerollSubAffectsTheObject():
	assert RerollSymbol() - 4 - 3


def test_rerollMultAffectsTheObject():
	assert RerollSymbol() * 3


def test_rerollDivAffectsTheObject():
	assert RerollSymbol() / 3


def test_rerollFloorDivAffectsTheObject():
	assert RerollSymbol() // 3


def test_rerollAddStrAffectsTheObject():
	assert RerollSymbol() + "a" + "b"


def test_rerollMixedSymbolsThrowError():
	with pytest.raises(TypeError):
		assert not ((RerollSymbol() + 4) + "a")


def test_rerollDefineDepth():
	q = RerollSymbolSpy(depth=4)
	assert q.getDepth() == 4

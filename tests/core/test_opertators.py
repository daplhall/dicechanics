from ttstatistics.core.genericmapping import GenericMapping
from ttstatistics.core.group import Group
from ttstatistics.core.operations.macro import Operators
from ttstatistics.core.operations.micro import add, max

performOnBag = Operators.performOnBag


def test_PerformOnBagWithOneItem(bagWithItems, simpleScalarDie):
	toTest = performOnBag(bagWithItems, add)
	assert {
		2: 0.0625,
		3: 0.25,
		4: 0.3750,
		5: 0.25,
		6: 0.0625,
	}.items() == toTest.items()


def test_PerformOnBagWithTwoItem(bagWithTwoItems):
	toTest = performOnBag(bagWithTwoItems, add)
	assert {2: 0.1, 3: 0.3, 4: 0.35, 5: 0.2, 6: 0.05}.items() == toTest.items()


def test_PerformOnBagWithFourItem(bagWithFourItems):
	toTest = performOnBag(bagWithFourItems, add)
	assert (
		toTest.items()
		== {
			4: 0.0256,
			5: 0.1024,
			6: 0.2048,
			7: 0.256,
			8: 0.2176,
			9: 0.128,
			10: 0.0512,
			11: 0.0128,
			12: 0.0016,
		}.items()
	)


def test_SelectiveAllFlat():
	d = GenericMapping(dict.fromkeys(range(1, 7), 1 / 6))
	bag = Group({d: 2})
	reference = performOnBag(bag, add)
	toTest = performOnBag(bag[:], add)
	assert toTest.items() == reference.items()


def test_SelectiveOnBagWithFourItem(bagWithTwoItems):
	reference = performOnBag(bagWithTwoItems, add)
	toTest = performOnBag(bagWithTwoItems[:], add)
	assert toTest.items() == reference.items()


def test_SelectiveOnBagWithFourItemMax(bagWithTwoItems):
	reference = performOnBag(bagWithTwoItems, max)
	toTest = performOnBag(bagWithTwoItems[:], max)
	assert toTest.items() == reference.items()


def test_SelectiveTwoItemsMaximum(bagWithTwoItems):
	reference = performOnBag(bagWithTwoItems, max)
	toTest = performOnBag(bagWithTwoItems[:1], add)
	assert toTest.items() == reference.items()


def test_SelectiveTwoItemsMinumum(bagWithTwoItems):
	reference = performOnBag(bagWithTwoItems, min)
	toTest = performOnBag(bagWithTwoItems[1:], add)
	assert toTest.items() == reference.items()


def test_SelectiveMixedMapping():
	d = GenericMapping({1: 1 / 3, 3: 1 / 3, 5: 1 / 3})
	g = GenericMapping({1: 1 / 4, 2: 1 / 4, 3: 1 / 4, 4: 1 / 4})
	bag = Group({d: 3, g: 2})
	reference = performOnBag(bag, add)
	toTest = performOnBag(bag[:], add)
	assert toTest.items() == reference.items()


"""
def test_SelectiveFourItemsMinumum(bagWithFourItems):
	toTest = performOnBag(bagWithFourItems[::2], add)
	assert toTest.items() == reference.items()
"""

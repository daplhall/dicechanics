from ttstatistics.core.genericmapping import GenericMapping
from ttstatistics.core.group import Group
from ttstatistics.core.operations.macro import Operators
from ttstatistics.core.operations.micro import add, max

selective = Operators.selectiveOnGroup
regular = Operators.regularOnGroup


def helperCompareTwoMappings(a, b):
	for (ref, refprob), (key, prob) in zip(a.items(), b.items()):
		assert ref == key
		assert round(refprob, 15) == round(prob, 15)


def test_PerformOnBagWithOneItem(groupWithItems, simpleScalarDie):
	toTest = regular(groupWithItems, add)
	assert {
		2: 0.0625,
		3: 0.25,
		4: 0.3750,
		5: 0.25,
		6: 0.0625,
	}.items() == toTest.items()


def test_PerformOnBagWithTwoItem(groupWithTwoItems):
	toTest = regular(groupWithTwoItems, add)
	ref = {2: 0.1, 3: 0.3, 4: 0.35, 5: 0.2, 6: 0.05}
	helperCompareTwoMappings(ref, toTest)


def test_PerformOnBagWithFourItem(groupWithFourItems):
	toTest = regular(groupWithFourItems, add)
	ref = {
		4: 0.0256,
		5: 0.1024,
		6: 0.2048,
		7: 0.256,
		8: 0.2176,
		9: 0.128,
		10: 0.0512,
		11: 0.0128,
		12: 0.0016,
	}
	helperCompareTwoMappings(ref, toTest)


def test_SelectiveAllFlat():
	d = GenericMapping(dict.fromkeys(range(1, 7), 1 / 6))
	group = Group({d: 2})
	reference = regular(group, add)
	toTest = selective(group[:], add)
	helperCompareTwoMappings(reference, toTest)


def test_SelectiveOnBagWithFourItem(groupWithTwoItems):
	reference = regular(groupWithTwoItems, add)
	toTest = selective(groupWithTwoItems[:], add)
	helperCompareTwoMappings(reference, toTest)


def test_SelectiveOnBagWithFourItemMax(groupWithTwoItems):
	reference = regular(groupWithTwoItems, max)
	toTest = selective(groupWithTwoItems[:], max)
	helperCompareTwoMappings(toTest, reference)


def test_SelectiveTwoItemsMaximum(groupWithTwoItems):
	reference = regular(groupWithTwoItems, max)
	toTest = selective(groupWithTwoItems[1:], add)
	helperCompareTwoMappings(reference, toTest)


def test_SelectiveTwoItemsMinumum(groupWithTwoItems):
	reference = regular(groupWithTwoItems, min)
	toTest = selective(groupWithTwoItems[:1], add)
	helperCompareTwoMappings(reference, toTest)


def test_SelectiveMixedMapping():
	d = GenericMapping({1: 1 / 3, 3: 1 / 3, 5: 1 / 3})
	g = GenericMapping({1: 1 / 4, 2: 1 / 4, 3: 1 / 4, 4: 1 / 4})
	group = Group({d: 3, g: 2})
	reference = regular(group, add)
	toTest = selective(group[:], add)
	helperCompareTwoMappings(toTest, reference)


def test_Selective2Lowest():
	d = GenericMapping({1: 1 / 3, 3: 1 / 3, 5: 1 / 3})
	group = Group({d: 3})
	toTest = selective(group[:2], add)
	reference = {
		2: 0.259259259259259,
		4: 0.333333333333333,
		6: 0.259259259259259,
		8: 0.111111111111111,
		10: 0.037037037037037,
	}
	helperCompareTwoMappings(reference, toTest)

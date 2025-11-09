from ttstatistics.core.operations.macro import Operators
from ttstatistics.core.operations.micro import add

perform = Operators.perform


def test_PerformOnBagWithOneItem(bagWithItems, simpleScalarDie):
	toTest = perform(bagWithItems, add)
	assert {
		2: 0.0625,
		3: 0.25,
		4: 0.3750,
		5: 0.25,
		6: 0.0625,
	}.items() == toTest.items()


def test_PerformOnBagWithTwoItem(bagWithTwoItems):
	toTest = perform(bagWithTwoItems, add)
	assert {2: 0.1, 3: 0.3, 4: 0.35, 5: 0.2, 6: 0.05}.items() == toTest.items()


def test_PerformOnBagWithFourItem(bagWithFourItems):
	toTest = perform(bagWithFourItems, add)
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

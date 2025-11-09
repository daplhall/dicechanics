import pytest

from ttstatistics.core.pool import Pool


def test_EmptyInit(emptyDie):
	assert not emptyDie


def test_MappingMeanScalar(simpleScalarDie, simpleScalarStatistical):
	assert simpleScalarDie.mean == simpleScalarStatistical.mean


def test_MappingMeanString(simpleStringDie):
	assert simpleStringDie.mean is None


def test_MappingVariansScalar(simpleScalarDie, simpleScalarStatistical):
	assert simpleScalarDie.varians == simpleScalarStatistical.varians


def test_MappingVariansString(simpleStringDie):
	assert simpleStringDie.varians is None


def test_MappingStdScalar(simpleScalarDie, simpleScalarStatistical):
	assert simpleScalarDie.std == simpleScalarStatistical.std


def test_MappingStdString(simpleStringDie):
	assert simpleStringDie.std is None


"""
def test_TwoDieMakeAPool(emptyDie):
	pool = emptyDie + emptyDie
	assert isinstance(pool, Pool)


def helper_CompareTwoMappings(toTestMapping, referenceMapping):
	for (key, value), (ref, refvalue) in zip(
		toTestMapping.items(), referenceMapping.items()
	):
		assert key == ref
		assert value == refvalue


def test_ScalarDieAddingScalar(
	simpleScalarDie, shiftedReferenceStatisticalDict
):
	helper_CompareTwoMappings(
		simpleScalarDie + 1, shiftedReferenceStatisticalDict
	)


def test_ScalarDieMultScalar(simpleScalarDie, referenceStatisticalDict):
	helper_CompareTwoMappings(simpleScalarDie * 1, referenceStatisticalDict)


def test_ScalarDieItems(simpleScalarDie, referenceStatisticalDict):
	helper_CompareTwoMappings(simpleScalarDie, referenceStatisticalDict)


def test_StringDieAddingString(simpleStringDie):
	helper_CompareTwoMappings(
		simpleStringDie + "a", {"aa": 1 / 4, "ab": 2 / 4, "ac": 1 / 4}
	)


def test_StringDieMultNum(simpleStringDie):
	helper_CompareTwoMappings(
		simpleStringDie * 2, {"aa": 1 / 4, "bb": 2 / 4, "cc": 1 / 4}
	)


def test_DieMappingCorrectly(simpleScalarDie, simpleScalarStatistical):
	def mapping(x):
		return x // 2

	reference = simpleScalarStatistical.map(mapping)
	die = simpleScalarDie.map(mapping)

	assert die.items() == reference.items()


def test_StringDieSubFailure(simpleStringDie):
	with pytest.raises(
		TypeError,
		match=r"unsupported operand type\(s\) for -: 'SortedString' and 'str'",
	):
		simpleStringDie - "a"


def test_ScalarDieSubtractingScalar(simpleScalarDie, downShiftedReferenceDict):
	helper_CompareTwoMappings(simpleScalarDie - 1, downShiftedReferenceDict)


def test_StringDieDivideFailure(simpleStringDie):
	with pytest.raises(
		TypeError,
		match=r"unsupported operand type\(s\) for /: 'SortedString' and 'str'",
	):
		simpleStringDie / "a"


def test_StringDieFloorDivideFailure(simpleStringDie):
	with pytest.raises(
		TypeError,
		match=r"unsupported operand type\(s\) for //: 'SortedString' and 'str'",
	):
		simpleStringDie // "a"


def test_ScalarDieDivideScalar(simpleScalarDie, simpleScalarStatistical):
	reference = simpleScalarStatistical.map(lambda x: x / 2)
	helper_CompareTwoMappings(simpleScalarDie / 2, reference)


def test_ScalarDieFloorDiv(simpleScalarDie, simpleScalarStatistical):
	reference = simpleScalarStatistical.map(lambda x: x // 2)
	helper_CompareTwoMappings(simpleScalarDie // 2, reference)

"""

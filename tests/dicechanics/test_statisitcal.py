import math
from collections import defaultdict

from ttstatistics.dicechanics.statisticals.scalar import ScalarStatistical


def test_baseEmptyInitialziation(emptyScalarStatistical):
	assert not emptyScalarStatistical


def test_baseSimpleInitiziation(simpleScalarStatistical):
	assert simpleScalarStatistical


def test_baseItemsReturnTheCorrectValue(
	referenceStatisticalDict, simpleScalarStatistical
):
	assert referenceStatisticalDict.items() == simpleScalarStatistical.items()


def test_baseValuesReturnTheCorrectValue(
	referenceStatisticalDict, simpleScalarStatistical
):
	for i, j in zip(
		referenceStatisticalDict.values(), simpleScalarStatistical.values()
	):
		assert round(i, 15) == round(j, 15)


def test_baseKeysReturnTheCorrectValue(
	referenceStatisticalDict, simpleScalarStatistical
):
	assert referenceStatisticalDict.keys() == simpleScalarStatistical.keys()


def test_baseMapValuesToHalf(simpleScalarStatistical, referenceStatisticalDict):
	def mapping(x):
		return x // 2

	unit = simpleScalarStatistical.map(mapping)
	reference = defaultdict(float)
	for key, value in referenceStatisticalDict.items():
		reference[mapping(key)] += value

	assert unit.items() == reference.items()


def meanCalulationHelper(reference):
	mean = 0
	for key, p in reference.items():
		mean += p * key
	return mean


def assertMean(statistical, referenceMean):
	return statistical.mean == referenceMean


def test_scalarMeanIsCorrect(simpleScalarStatistical, referenceStatisticalDict):
	mean = meanCalulationHelper(referenceStatisticalDict)
	return simpleScalarStatistical.mean == mean


def test_stringMeanIsCorrect(simpleStringStatistical):
	assert simpleStringStatistical.mean is None


def variansCalulationHelper(reference):
	mean = meanCalulationHelper(reference)
	return sum((key - mean) ** 2 for key in reference)


def test_scalarVariansIsCorrect(
	simpleScalarStatistical, referenceStatisticalDict
):
	var = variansCalulationHelper(referenceStatisticalDict)
	return simpleScalarStatistical.varians == var


def test_stringVariansIsCorrect(simpleStringStatistical):
	assert simpleStringStatistical.varians is None


def test_scalarStandardDeviationIsCorrect(
	simpleScalarStatistical, referenceStatisticalDict
):
	var = variansCalulationHelper(referenceStatisticalDict)
	return simpleScalarStatistical.std == math.sqrt(var)


def test_stringStandardDeviationIsCorrect(simpleStringStatistical):
	assert simpleStringStatistical.std is None


def test_scalarStatisticalNormalize(referenceStatisticalDict):
	data: dict[int, int] = {1: 1, 2: 2, 3: 1}
	q = ScalarStatistical(data).normalize()
	assert q.items() == referenceStatisticalDict.items()

from ttstatistics.core.empty import VariableCount
from ttstatistics.core.mapping import GenericMapping, expand


def test_GenericMappingIsEmptyOnEmptyInit():
	assert not GenericMapping()


def test_GenericMappingIsNotEmptyInit(referenceStatisticalDict):
	assert GenericMapping(referenceStatisticalDict)


def CompareItemsBetweenTwoMappings(toTestMapping, referenceMapping):
	for (key, value), (ref, refvalue) in zip(
		toTestMapping.items(), referenceMapping.items()
	):
		if isinstance(key, VariableCount) and isinstance(key, VariableCount):
			assert True
		else:
			assert key == ref
		assert abs(value - refvalue) < 1e-15


def CompareKeysBetweenTwoMappings(toTestMapping, referenceMapping):
	for key, ref in zip(toTestMapping.keys(), referenceMapping.keys()):
		assert key == ref


def CompareValuesBetweenTwoMappings(toTestMapping, referenceMapping):
	for value, refvalue in zip(
		toTestMapping.values(), referenceMapping.values()
	):
		assert value == refvalue


def test_GenericMappingItemsAreCorrect(referenceStatisticalDict):
	CompareItemsBetweenTwoMappings(
		GenericMapping(referenceStatisticalDict), referenceStatisticalDict
	)


def test_GenericMappingKeysAreCorrect(referenceStatisticalDict):
	CompareKeysBetweenTwoMappings(
		GenericMapping(referenceStatisticalDict), referenceStatisticalDict
	)


def test_GenericMappingValuesAreCorrect(referenceStatisticalDict):
	CompareValuesBetweenTwoMappings(
		GenericMapping(referenceStatisticalDict), referenceStatisticalDict
	)


def test_Expand():
	ref = {1: 7 / 24, 2: 7 / 24, 3: 7 / 24, 4: 3 / 24}
	m4 = GenericMapping({1: 1 / 4, 2: 1 / 4, 3: 1 / 4, 4: 1 / 4})
	m3 = GenericMapping({1: 1 / 3, 2: 1 / 3, 3: 1 / 3})
	res = expand(GenericMapping({m4: 1 / 2, m3: 1 / 2}))
	CompareItemsBetweenTwoMappings(ref, res)


def test_ExpandWithEmpty():
	m4 = GenericMapping({1: 1 / 4, 2: 1 / 4, 3: 1 / 4, 4: 1 / 4})
	m3 = GenericMapping({VariableCount(m4): 0, 1: 1 / 3, 2: 1 / 3, 3: 1 / 3})
	res = expand(GenericMapping({m3: 1}))
	CompareItemsBetweenTwoMappings(res, m3)


def test_ExpandWithEmptyMutliple():
	m4 = GenericMapping({1: 1 / 4, 2: 1 / 4, 3: 1 / 4, 4: 1 / 4})
	m3 = GenericMapping({VariableCount(m4): 0, 1: 1 / 3, 2: 1 / 3, 3: 1 / 3})
	res = expand(GenericMapping({m3: 1 / 2, m4: 1 / 2}))
	ref = {VariableCount(m4): 0, 1: 7 / 24, 2: 7 / 24, 3: 7 / 24, 4: 3 / 24}
	CompareItemsBetweenTwoMappings(res, ref)

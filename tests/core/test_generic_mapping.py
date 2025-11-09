from ttstatistics.core.genericmapping import GenericMapping


def test_GenericMappingIsEmptyOnEmptyInit():
	assert not GenericMapping()


def test_GenericMappingIsNotEmptyInit(referenceStatisticalDict):
	assert GenericMapping(referenceStatisticalDict)


def CompareItemsBetweenTwoMappings(toTestMapping, referenceMapping):
	for (key, value), (ref, refvalue) in zip(
		toTestMapping.items(), referenceMapping.items()
	):
		assert key == ref
		assert value == refvalue


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

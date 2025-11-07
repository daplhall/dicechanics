from dicechanics.pool import Pool


def test_EmptyInit(emptyDie):
	assert not emptyDie


def test_DieMeanScalar(simpleScalarDie, simpleScalarStatistical):
	assert simpleScalarDie.mean == simpleScalarStatistical.mean


def test_DieMeanString(simpleStringDie):
	assert simpleStringDie.mean is None


def test_DieVariansScalar(simpleScalarDie, simpleScalarStatistical):
	assert simpleScalarDie.varians == simpleScalarStatistical.varians


def test_DieVariansString(simpleStringDie):
	assert simpleStringDie.varians is None


def test_DieStdScalar(simpleScalarDie, simpleScalarStatistical):
	assert simpleScalarDie.std == simpleScalarStatistical.std


def test_DieStdString(simpleStringDie):
	assert simpleStringDie.std is None


def test_TwoDieMakeAPool(emptyDie):
	pool = emptyDie + emptyDie
	assert isinstance(pool, Pool)


def test_ScalarDieAddingScalar(
	simpleScalarDie, shiftedReferenceStatisticalDict
):
	shiftedDie = simpleScalarDie + 1
	for (key, value), (ref, refvalue) in zip(
		shiftedDie.items(), shiftedReferenceStatisticalDict.items()
	):
		assert key == ref
		assert value == refvalue


def test_ScalarDieMultScalar(simpleScalarDie, referenceStatisticalDict):
	shiftedDie = simpleScalarDie * 1
	for (key, value), (ref, refvalue) in zip(
		shiftedDie.items(), referenceStatisticalDict.items()
	):
		assert key == ref
		assert value == refvalue


def test_ScalarDieItems(simpleScalarDie, referenceStatisticalDict):
	for (key, val), (refkey, refval) in zip(
		simpleScalarDie.items(), referenceStatisticalDict.items()
	):
		assert key == refkey
		assert val == refval


def test_StringDieAddingString(simpleStringDie):
	shiftedDie = simpleStringDie + "a"
	referenceString = {"aa": 1, "ab": 1, "ac": 1}
	for (key, _), (ref, _) in zip(shiftedDie.items(), referenceString.items()):
		assert key == ref


def test_StringDieMultNum(simpleStringDie):
	shiftedDie = simpleStringDie * 2
	referenceString = {"aa": 1, "bb": 1, "cc": 1}
	for (key, _), (ref, _) in zip(shiftedDie.items(), referenceString.items()):
		assert key == ref

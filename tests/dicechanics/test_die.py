from ttstatistics.dicechanics.die import Die
from ttstatistics.dicechanics.statisticals.scalar import ScalarStatistical
from ttstatistics.dicechanics.symbolics import reroll


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


def test_DieAddScalarInt(simpleScalarDie):
	d = simpleScalarDie + 1
	ref = {2: 1 / 4, 3: 2 / 4, 4: 1 / 4}
	assert d.items() == ref.items()


def test_DieAddScalarDie(simpleScalarDie):
	d = simpleScalarDie + simpleScalarDie
	ref = {2: 1 / 16, 3: 4 / 16, 4: 6 / 16, 5: 4 / 16, 6: 1 / 16}
	assert d.items() == ref.items()


def test_DieSubScalarInt(simpleScalarDie):
	d = simpleScalarDie - 1
	ref = {0: 1 / 4, 1: 2 / 4, 2: 1 / 4}
	assert d.items() == ref.items()


def test_DieSubScalarDie(simpleScalarDie):
	d = simpleScalarDie - simpleScalarDie
	ref = {-2: 1 / 16, -1: 4 / 16, 0: 6 / 16, 1: 4 / 16, 2: 1 / 16}
	q = dict(sorted(d.items(), key=lambda x: x[0]))
	assert ref.items() == q.items()


def test_DieMulScalarInt(simpleScalarDie):
	d = simpleScalarDie * 1
	ref = {1: 1 / 4, 2: 2 / 4, 3: 1 / 4}
	assert d.items() == ref.items()


def test_DieMulScalarDie(simpleScalarDie):
	d = simpleScalarDie * simpleScalarDie
	ref = {1: 1 / 16, 2: 4 / 16, 3: 2 / 16, 4: 4 / 16, 6: 4 / 16, 9: 1 / 16}
	q = dict(sorted(d.items(), key=lambda x: x[0]))
	assert ref.items() == q.items()


def test_DieDivScalarInt(simpleScalarDie):
	d = simpleScalarDie // 2
	ref = {0: 1 / 4, 1: 3 / 4}
	assert d.items() == ref.items()


def test_DieDivScalarDie(simpleScalarDie):
	d = simpleScalarDie // simpleScalarDie
	ref = {0: 5 / 16, 1: 8 / 16, 2: 2 / 16, 3: 1 / 16}
	q = dict(sorted(d.items(), key=lambda x: x[0]))
	assert ref.items() == q.items()


def test_DieTrueDivScalarInt(simpleScalarDie):
	d = simpleScalarDie / 2
	ref = {0.5: 1 / 4, 1: 2 / 4, 1.5: 1 / 4}
	assert d.items() == ref.items()


def test_DieTrueDivScalarDie(simpleScalarDie):
	d = simpleScalarDie / simpleScalarDie
	ref = {
		1 / 3: 1 / 16,
		0.5: 2 / 16,
		2 / 3: 2 / 16,
		1: 6 / 16,
		1.5: 2 / 16,
		2.0: 2 / 16,
		3.0: 1 / 16,
	}
	q = dict(sorted(d.items(), key=lambda x: x[0]))
	assert ref.items() == q.items()


def test_DieInDie(d4):
	g = Die(ScalarStatistical({1: 1 / 4, 2: 1 / 4, 3: 1 / 4, d4: 1 / 4}))
	ref = {1: 5 / 16, 2: 5 / 16, 3: 5 / 16, 4: 1 / 16}
	assert ref.items() == g.items()


def test_2DieInDie(d4):
	g = Die(ScalarStatistical({1: 1 / 4, 2: 1 / 4, 3: 1 / 4, 5: 1 / 4}))
	g = Die(ScalarStatistical({1: 1 / 4, 2: 1 / 4, g: 1 / 4, d4: 1 / 4}))
	ref = {1: 6 / 16, 2: 6 / 16, 3: 2 / 16, 4: 1 / 16, 5: 1 / 16}
	assert ref.items() == g.items()


def test_DieInDieScewed(d4):
	g = Die(ScalarStatistical({1: 1 / 4, 2: 1 / 4, d4: 2 / 4}))
	ref = {1: 6 / 16, 2: 6 / 16, 3: 2 / 16, 4: 2 / 16}
	assert ref.items() == g.items()


def test_DieCountFaces(d4):
	count = d4.count(4)
	ref = {0: 3 / 4, 1: 1 / 4}
	assert ref.items() == count.items()


def test_DieCountMultipleFaces(d4):
	count = d4.count(2, 3, 4)
	ref = {0: 1 / 4, 1: 3 / 4}
	assert ref.items() == count.items()


def test_DieRerollOne(d4):
	reroll = d4.reroll(4)
	ref = {1: 5 / 16, 2: 5 / 16, 3: 5 / 16, 4: 1 / 16}
	assert ref.items() == reroll.items()


def test_DieRerollMultiple(d4):
	reroll = d4.reroll(3, 4)
	ref = {1: 6 / 16, 2: 6 / 16, 3: 2 / 16, 4: 2 / 16}
	assert ref.items() == reroll.items()


def test_MapRerollIsTheSame(d4):
	def f(outcome):
		if outcome == 4:
			return d4
		else:
			return outcome

	mapReroll = d4.map(f)
	reroll = d4.reroll(4)
	assert mapReroll.items() == reroll.items()


def test_RerollDepth2(d4):
	rerolled = d4.reroll(4, depth=2)
	ref = {1: 21 / 64, 2: 21 / 64, 3: 21 / 64, 4: 1 / 64}
	assert rerolled.items() == ref.items()


def test_MapRerollMutlipleTimes(d4):
	def f(outcome):
		if outcome == 4:
			return d4
		else:
			return outcome

	mapReroll = d4.map(f)
	mapReroll = mapReroll.map(f)
	ref = {1: 21 / 64, 2: 21 / 64, 3: 21 / 64, 4: 1 / 64}
	assert mapReroll.items() == ref.items()


def test_StringReprentation(d4):
	assert str(d4) == (
		"Die with mu - 2.50, sigma - 2.24\n--------------------------------\n"
		"1|#################### 25.00%\n2|#################### 25.00%\n"
		"3|#################### 25.00%\n4|#################### 25.00%\n"
	)

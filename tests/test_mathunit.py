from dicechanics.baseunits.combinationsunit import CombinationsUnit


def test_add(StandardMathUnit):
	unit1 = StandardMathUnit + StandardMathUnit
	unit1.simplify()
	res = CombinationsUnit({2: 1, 4: 4, 6.5: 2, 6: 4, 8.5: 4, 11.0: 1})
	assert unit1 == res


def test_add_num(StandardMathUnit):
	unit = StandardMathUnit + 1
	assert unit.outcomes == [2, 4, 6.5]


def test_sub_num(StandardMathUnit):
	unit = StandardMathUnit - 1
	assert unit.outcomes == [0, 2, 4.5]


def test_lsub_num(StandardMathUnit):
	unit = 1 - StandardMathUnit
	assert unit.outcomes == [-4.5, -2, 0]


def test_mul_num(StandardMathUnit):
	unit = StandardMathUnit * 2
	assert unit.outcomes == [2, 6, 11]


def test_lmul_num(StandardMathUnit):
	unit = 2 * StandardMathUnit
	assert unit.outcomes == [2, 6, 11]


def test_neg_num(StandardMathUnit):
	unit = -StandardMathUnit
	assert unit.outcomes == [-5.5, -3, -1]


def test_pos_num(StandardMathUnit):
	unit = +StandardMathUnit
	assert unit.outcomes == [1, 3, 5.5]


# TODO take dices test and rewrite to mathunit

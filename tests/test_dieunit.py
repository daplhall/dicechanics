from dicechanics.baseunits.DieUnit import DieUnit


def test_dice_expansion():
	d = DieUnit({1: 1, 2: 1, 3: 1, 4: 1})
	p = DieUnit({2: 1, 1: 2, d: 1})
	assert p.data == {1: 9, 2: 5, 3: 1, 4: 1}

import ttstatistics.dicechanics as ds


def test_InterfaceIntInput():
	d = ds.d(6)
	ref = dict.fromkeys(range(1, 7), 1 / 6)
	assert d.items() == ref.items()


def test_InterfaceDictInput():
	d = ds.d(dict.fromkeys(range(1, 7), 1 / 6))
	ref = dict.fromkeys(range(1, 7), 1 / 6)
	assert d.items() == ref.items()


def test_InterfaceStrInput():
	ref = {"a": 1 / 3, "2": 1 / 3, "3": 1 / 3}
	d = ds.d(ref)
	assert d.items() == ref.items()


def test_InterfaceListInput():
	d = ds.d([1, 2, 3, 4, 5, 6])
	ref = dict.fromkeys(range(1, 7), 1 / 6)
	assert d.items() == ref.items()


def test_InterfaceParserSimple(d4):
	d = ds.d("1")
	ref = {1: 1}
	assert d.items() == ref.items()


def test_InterfaceParserExpand(d4):
	d = ds.d("1..4")
	assert d.items() == d4.items()


def test_InterfaceParserRepeat():
	d = ds.d("1:4")
	ref = {1: 1}
	assert d.items() == ref.items()


def test_InterfaceParserExpandRepeat():
	d = ds.d("1..3:4")
	ref = {1: 1 / 3, 2: 1 / 3, 3: 1 / 3}
	assert d.items() == ref.items()


def test_InterfaceParserMultiple():
	d = ds.d("1:3,4:2,5..8")
	ref = {1: 3 / 9, 4: 2 / 9, 5: 1 / 9, 6: 1 / 9, 7: 1 / 9, 8: 1 / 9}
	assert d.items() == ref.items()


"""
def test_InterfaceStrInParserSingle():
	d = ds.d("a")
	ref = {"a": 1}
	assert d.items() == ref.items()
"""

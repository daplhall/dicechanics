from ttstatistics.core import protocols


def test_emptyBagIsEmpty(emptyBag):
	assert not emptyBag


def test_bagNotEmpty(bagWithItems):
	assert bagWithItems


def test_addMappingToBag(emptyBag, emptyDie):
	assert emptyBag + emptyDie


def test_addBagToBag(emptyBag, emptyDie):
	base = emptyBag + emptyDie
	toCheck = base + base
	assert all(
		isinstance(mapping, protocols.Mapping) for mapping in toCheck.keys()
	)


def test_bagHasItemsCheckedWithItems(emptyBag, emptyDie):
	base = emptyBag + emptyDie
	for key, value in base.items():
		assert key == emptyDie


def test_bagHasItemCheckedWithKeys(emptyBag, emptyDie):
	base = emptyBag + emptyDie
	for key in base.keys():
		assert key == emptyDie


def test_bagHasItemCheckedWithValues(emptyBag, emptyDie):
	base = emptyBag + emptyDie
	for key in base.values():
		assert key == 1

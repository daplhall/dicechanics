from ttstatistics.core import protocols


def test_emptyBagIsEmpty(emptyBag):
	assert not emptyBag


def test_bagNotEmpty(bagWithItems):
	assert bagWithItems


def test_addMappingToBag(emptyBag, emptyDict):
	assert emptyBag + emptyDict


def test_addBagToBag(emptyBag, emptyDict):
	base = emptyBag + emptyDict
	toCheck = base + base
	assert all(
		isinstance(mapping, protocols.Mapping) for mapping in toCheck.keys()
	)


def test_bagHasItemsCheckedWithItems(emptyBag, emptyDict):
	base = emptyBag + emptyDict
	for key, value in base.items():
		assert key == emptyDict


def test_bagHasItemCheckedWithKeys(emptyBag, emptyDict):
	base = emptyBag + emptyDict
	for key in base.keys():
		assert key == emptyDict


def test_bagHasItemCheckedWithValues(emptyBag, emptyDict):
	base = emptyBag + emptyDict
	for key in base.values():
		assert key == 1

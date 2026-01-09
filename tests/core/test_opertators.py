import pytest

from ttstatistics.core.group import Group
from ttstatistics.core.mapping import GenericMapping
from ttstatistics.core.operations import (
	add,
	max,
	regularOnGroup,
	selectiveOnGroup,
)

selective = selectiveOnGroup
regular = regularOnGroup


def compareMappings(a, b):
	if not (a and b):
		assert 0 == 1
	for key, prop in a.items():
		assert abs(b[key] - prop) < 1e-15


@pytest.mark.parametrize(
	("Group", "Ref"),
	[
		(
			"Group2Dublicate",
			{2: 0.0625, 3: 0.25, 4: 0.3750, 5: 0.25, 6: 0.0625},
		),
		(
			"Group2Items",
			{2: 0.1, 3: 0.3, 4: 0.35, 5: 0.2, 6: 0.05},
		),
		(
			"Group4Items",
			{
				4: 0.0256,
				5: 0.1024,
				6: 0.2048,
				7: 0.256,
				8: 0.2176,
				9: 0.128,
				10: 0.0512,
				11: 0.0128,
				12: 0.0016,
			},
		),
	],
)
def test_PerformOnBag(request, Group, Ref):
	group = request.getfixturevalue(Group)
	compareMappings(regular(group, add), Ref)


def test_SelectiveAllFlat():
	d = GenericMapping(dict.fromkeys(range(1, 7), 1 / 6))
	group = Group({d: 2})
	reference = regular(group, add)
	toTest = selective(group[:], add)
	compareMappings(reference, toTest)


@pytest.mark.parametrize(
	("Group", "regOps", "selOps", "slice_"),
	[
		("Group2Items", add, add, slice(0, None)),
		("Group2Items", max, max, slice(0, None)),
		("Group2Items", max, add, slice(1, None)),
		("Group2Items", min, add, slice(1)),
		("GroupMixed", add, add, slice(0, None)),
	],
)
def test_CombationsParaity(request, Group, regOps, selOps, slice_):
	group = request.getfixturevalue(Group)
	compareMappings(regular(group, regOps), selective(group[slice_], selOps))


@pytest.mark.parametrize(
	("Group", "slice_", "ref"),
	[
		(
			"GroupOddValues3",
			slice(0, 2, None),
			{
				2: 0.259259259259259,
				4: 0.333333333333333,
				6: 0.259259259259259,
				8: 0.111111111111111,
				10: 0.037037037037037,
			},
		),
		(
			"Group3Flat6",
			slice(-2, None, None),
			{
				2: 0.0046296296296296285,
				3: 0.013888888888888888,
				4: 0.032407407407407406,
				5: 0.05555555555555555,
				6: 0.08796296296296297,
				7: 0.125,
				8: 0.1574074074074074,
				9: 0.16666666666666666,
				10: 0.15740740740740738,
				11: 0.125,
				12: 0.07407407407407406,
			},
		),
	],
)
def test_Selective(request, Group, slice_, ref):
	group = request.getfixturevalue(Group)
	compareMappings(selective(group[slice_], add), ref)

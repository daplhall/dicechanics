import pytest

from fixtures.mapping import MappingMock
from ttstatistics.core.group import Group
from ttstatistics.core.groupcount import GroupCountFactory, GroupCountTypes


@pytest.fixture
def GroupEmpty():
	return Group()


@pytest.fixture
def Group2Dublicate(simpleScalarMock):
	Count = GroupCountFactory().create(GroupCountTypes.int)
	return Group({simpleScalarMock: Count(2)})


@pytest.fixture
def Group2Items(simpleScalarMock, AltScalarMock):
	Count = GroupCountFactory().create(GroupCountTypes.int)
	return Group({simpleScalarMock: Count(1), AltScalarMock: Count(1)})


@pytest.fixture
def Group4Items(alternativeReferenceDict):
	a = MappingMock(alternativeReferenceDict)
	b = MappingMock(alternativeReferenceDict)
	c = MappingMock(alternativeReferenceDict)
	Count = GroupCountFactory().create(GroupCountTypes.int)
	return Group(
		{
			a: Count(2),
			b: Count(1),
			c: Count(1),
		}
	)


@pytest.fixture
def Group3Flat6(FlatMapping6):
	Count = GroupCountFactory().create(GroupCountTypes.int)
	return Group({FlatMapping6: Count(3)})


@pytest.fixture
def GroupMixed(FlatMapping3, FlatMapping4):
	Count = GroupCountFactory().create(GroupCountTypes.int)
	return Group({FlatMapping3: Count(3), FlatMapping4: Count(2)})


@pytest.fixture
def GroupOddValues3(FlatMappingOdd3Values):
	Count = GroupCountFactory().create(GroupCountTypes.int)
	return Group({FlatMappingOdd3Values: Count(3)})

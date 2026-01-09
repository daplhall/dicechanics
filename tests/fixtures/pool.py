import pytest

from ttstatistics.core.groupcount import GroupCountFactory, GroupCountTypes
from ttstatistics.dicechanics.pool import Pool


@pytest.fixture
def pool3d6(d6):
	Count = GroupCountFactory().create(GroupCountTypes.int)
	return Pool({d6: Count(3)})

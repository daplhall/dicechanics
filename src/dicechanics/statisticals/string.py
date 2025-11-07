from dicechanics.primitives import SortedString
from dicechanics.statisticals.base import BaseStatistical


class StringStatistical(BaseStatistical):
	def __init__(self, data: dict[str, float] = {}, Stringifyer=SortedString):
		super().__init__(
			{Stringifyer(key): value for key, value in data.items()}
		)

	@property
	def mean(self):
		return None

	@property
	def varians(self):
		return None

	@property
	def std(self):
		return None

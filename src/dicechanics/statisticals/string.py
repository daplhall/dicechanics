from dicechanics.statisticals.base import BaseStatistical


class StringStatistical(BaseStatistical):
	def __init__(self, data: dict[str, float] = {}):
		super().__init__(data)

	@property
	def mean(self):
		return None

	@property
	def varians(self):
		return None

	@property
	def std(self):
		return None

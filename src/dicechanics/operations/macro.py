from dicechanics.operations.combinatorics import combinations
from dicechanics.utils.reference import Reference


class Operators:
	@staticmethod
	def perform(bag, operation):
		res = combinations(list(bag.items()), operation, 0, Reference(None))
		norm = sum(res.values())
		q = {key: round(value / norm, 15) for key, value in res.items()}
		return type(bag)(q)

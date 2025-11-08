from dicechanics.operations.combinatorics import Combinatorics
from dicechanics.utils.reference import Reference


class Operators:
	@staticmethod
	def perform(bag, operation):
		res = Combinatorics.combinations(
			list(bag.items()), operation, 0, Reference(None)
		)
		norm = sum(res.values())
		q = {key: round(value / norm, 15) for key, value in res.items()}
		return type(bag)(q)


"""
	res = defaultdict(lambda: 1)
	for mapping, count in bag.items():
		for key, value in mapping.items():
			res[key] *= value * count
	norm = sum(res.values())
	return type(bag)({key: value / norm for key, value in res.items()})
"""

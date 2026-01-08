from ttstatistics.core.protocols import Mapping


class VariableCount:
	"""
	when included in a mapping it should always have 0 as properbility
	"""

	def __init__(self, mapping: Mapping):
		self.max = max(mapping.keys())
		self.counts = mapping
		# self.counts = {
		# (self.max - key): value for key, value in mapping.items()
		# }

	def __hash__(self):
		return hash(tuple(self.counts.items()))

	def __add__(self, other):
		return self.max + other

	def __radd__(self, other):
		return self + other

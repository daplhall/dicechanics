from ttstatistics.core.protocols import Mapping


class VariableCount:
	"""
	when included in a mapping it should always have 0 as properbility
	"""

	def __init__(self, mapping: Mapping):
		self.max = max(mapping.keys())
		# self.counts = mapping
		self.counts = {
			(self.max - key): value for key, value in mapping.items()
		}

	def __hash__(self):
		return hash(tuple(self.counts.items()))

	def __lt__(self, other):
		return True

	def __le__(self, other):
		return True

	def __gt__(self, other):
		return False

	def __ge__(self, other):
		return False

	def __eq__(self, other):
		return False

	def __add__(self, other):
		return self.max + other

	def __radd__(self, other):
		return self + other

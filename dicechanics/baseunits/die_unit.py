from dicechanics.baseunits.mathops_unit import MathOpsUnit


class DieUnit(MathOpsUnit):
	def __init__(self, data=None, /, **kwargs):
		super().__init__(data, **kwargs)

	f = super().outcomes

	def reroll(self, redo, depth=1):
		return NotImplemented

	def _plode(self, ops, ploder, depth=1):
		return NotImplemented

	def explode(self, exploder, depth=1):
		return NotImplemented

	def implode(self, imxploder, depth=1):
		return NotImplemented

	def count(self, targets):
		return NotImplemented

	def folding(self, rhs, ops, into):
		return NotImplemented

	def fold_over(self, rhs, /, into):
		return NotImplemented

	def fold_under(self, rhs, /, into):
		return NotImplemented

	def nrolls(self, rhs, ops):
		return NotImplemented

	def __call__(self, mapping):
		return NotImplemented

	def __rmatmul__(self, lhs):
		return NotImplemented

	def __matmul__(self, lhs):
		return NotImplemented

	def __str__(self):
		pass

	def __repr__(self):
		pass

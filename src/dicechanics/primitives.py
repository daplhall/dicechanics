class SortedString(str):
	def __new__(cls, value):
		return str.__new__(cls, "".join(sorted(value)))

	def __add__(self, lhs):
		return type(self)(super().__add__(lhs))

	def __mul__(self, lhs):
		return type(self)(super().__mul__(lhs))


# https://stackoverflow.com/questions/19886385/python-can-i-have-a-subclass-return-instances-of-its-own-type-for-operators-def

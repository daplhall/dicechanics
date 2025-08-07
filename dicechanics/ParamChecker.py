import inspect
from typing import Tuple


def option_checker(option, arg, acpt_crit=0.7) -> Tuple[bool, float]:
	soption = set(option)
	prcnt_match = len(soption & set(arg)) / len(soption)
	return True if prcnt_match >= acpt_crit else False, prcnt_match


class ParamChecker:
	"""
	this could be a function wrapper?
	"""

	def __init__(self, template_function):
		self.options = ParamChecker.signature(template_function)
		self.with_types = False

	def check(self, function):
		missing = self.options.copy()
		for param, typing in ParamChecker.signature(function).items():
			pass

	@staticmethod
	def signature(template):
		return {
			param.name: param.annotation
			for param in inspect.signature(template).parameters.values()
		}

	@classmethod
	def typing(cls, template_function):
		self = cls(template_function)
		self.with_types = True
		return self


@ParamChecker
def test_template(x, y, maximum, minimum):
	pass


@ParamChecker.typing
def test_template_types(x, y: object, maximum: int, minimum: float):
	pass


print(test_template.options)
print(test_template_types.options)


def main():
	option = "maximum"
	arg = "maxi"
	res = option_checker(option, arg)
	print(res)


if __name__ == "__main__":
	main()

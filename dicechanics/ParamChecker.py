import inspect
from typing import Tuple


class OptionsMatcher:
	"""
	needs to contain options
	Idea:
	https://en.wikipedia.org/wiki/Levenshtein_distance
	https://stackoverflow.com/questions/5859561/getting-the-closest-string-match
	"""

	def __init__(self, options: dict):
		self.options = {i: set(i) for i in options.keys()}

	def match(self, arg, acpt_crit=0.7) -> Tuple[bool, float]:
		""" """
		tmp = []
		for option, matcher in self.options.items():
			prcnt_match = len(matcher & set(arg)) / len(matcher)
			if prcnt_match >= acpt_crit:
				tmp.append((option, prcnt_match))
		tmp.sort(key=lambda key: key[1], reverse=True)
		return [i for i, _ in tmp]


class Signature:
	"""Collects signature"""

	def __init__(self, template_function):
		self.options = Signature.signature(template_function)

	@staticmethod
	def signature(template):
		return {
			param.name: param.annotation
			for param in inspect.signature(template).parameters.values()
		}


class ParamChecker(Signature):
	def __init__(self, function):
		super().__init__(function)
		self.matcher = OptionsMatcher(self.options)
		self.with_types = False

	def check(self, function):
		"""
		TODO I am not checking fully illegals
		"""
		wrong_type = []
		params = ParamChecker.signature(function)
		missing = set(params) - set(self.options)
		hits = set(params) & set(self.options)
		if self.with_types:
			options = filter(lambda x: x[0] in hits, params.items())
			for param, mytype in options:
				if mytype != self.options[param]:
					wrong_type.append((param, mytype, self.options[param]))
		my_matches = []
		for miss in missing:
			if matches := self.matcher.match(miss):
				my_matches.append((miss, matches))
		# TODO make Exception raising its own special exception
		msg = ""
		if wrong_type:
			for param, curr_type, corr_type in wrong_type:
				msg += f"Wrong Type - Parameter {param}\n"
				msg += f"\t it is '{curr_type.__name__}' it should be '{corr_type.__name__}'\n"
		if my_matches:
			for written, matches in my_matches:
				msg += f"Parameter {written} is not supported, did you mean:\n"
				for match in matches:
					msg += f"\t- {match}\n"
		if msg:
			raise Exception(
				f"\nError in the signature of '{function.__name__}' in {inspect.getsoucefile(function)}\n"
				+ msg
			)
		return True

	@classmethod
	def with_typing(cls, template_function):
		self = cls(template_function)
		self.with_types = True
		return self


@ParamChecker
def test_template(x, y, maximum, minimum):
	pass


@ParamChecker
def test_template_empty():
	pass


@ParamChecker.with_typing
def test_template_types(x, y: object, maximum: int, minimum: float):
	pass


print(test_template.options)
print(test_template_types.options)
print(test_template_empty.options)
print("================")


def sanity(x, y, maimum, minim):
	pass


test_template.check(sanity)


if __name__ == "__main__":
	pass

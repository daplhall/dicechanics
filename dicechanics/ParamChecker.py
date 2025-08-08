import inspect
from typing import Tuple

"""
the idea is that when pool is used as a decorator we do a check on the function

if you want to do it with a perform, its a good idea to use @pool_func decorator
which checks it for you when the function is defined
"""


def lev(a: str, b: str):
	"""
	levenshtein_distance
	https://en.wikipedia.org/wiki/Levenshtein_distance
	"""
	if len(b) == 0:
		return len(a)
	elif len(a) == 0:
		return len(b)
	elif a[0] == b[0]:
		return lev(a[1:], b[1:])
	else:
		return 1 + min(lev(a[1:], b), lev(a, b[1:]), lev(a[1:], b[1:]))


class OptionsMatcher:
	"""
	needs to contain options
	Idea:
	https://stackoverflow.com/questions/5859561/getting-the-closest-string-match
	"""

	def __init__(self, options: dict):
		self.options = options

	def match(self, arg) -> Tuple[bool, float]:
		""" """
		tmp = []
		for option in self.options:
			tmp.append((lev(option, arg), option))
		tmp.sort()
		return [i[1] for i in tmp if min(tmp)[0] == i[0]]


class Signature:
	"""Collects signature"""

	@staticmethod
	def signature(template):
		return {
			param.name: param.annotation
			for param in inspect.signature(template).parameters.values()
		}


class ParamChecker(OptionsMatcher, Signature):
	def __init__(self, func_prototype):
		super().__init__(ParamChecker.signature(func_prototype))
		self.with_types = False

	def check(self, function) -> set:
		wrong_types = []
		params = ParamChecker.signature(function)
		missing = set(params) - set(self.options)
		hits = set(params) & set(self.options)
		if self.with_types:
			options = filter(lambda x: x[0] in hits, params.items())
			for param, mytype in options:
				if mytype != self.options[param]:
					wrong_types.append((param, mytype, self.options[param]))
		my_matches = []
		for miss in missing:
			if matches := self.match(miss):
				my_matches.append((miss, matches))
		if my_matches or wrong_types:
			raise UnsupportedParameters(my_matches, wrong_types, function)
		return hits

	@classmethod
	def with_typing(cls, template_function):
		self = cls(template_function)
		self.with_types = True
		return self


class UnsupportedParameters(Exception):
	def __init__(self, matches, wrong_types, function):
		msg = ""
		if wrong_types:
			for param, curr_type, corr_type in wrong_types:
				msg += f"* Wrong Type - Parameter {param}\n"
				msg += f"\t it is '{curr_type.__name__}' "
				f"it should be '{corr_type.__name__}'\n"
		if matches:
			for written, match in matches:
				msg += (
					f"* Parameter '{written}' is not supported, did you mean:\n"
				)
				for suggestion in match:
					msg += f"\t- {suggestion}\n"
		super().__init__(
			f"\nError in the signature of '{function.__name__}'"
			"in {inspect.getsourcefile(function)}\n" + msg
		)

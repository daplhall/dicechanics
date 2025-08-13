import inspect

"""
the idea is that when pool is used as a decorator we do a check on the function

if you want to do it with a perform, its a good idea to use @pool_func decorator
which checks it for you when the function is defined
"""


class OptionsMatcher:
	"""
	needs to contain options
	Idea:
	https://stackoverflow.com/questions/5859561/getting-the-closest-string-match
	"""

	def __init__(self, options: dict):
		self._options = options

	def match(self, arg: str) -> list[str]:
		""" """
		tmp = []
		for option in self.options:
			tmp.append((OptionsMatcher.lev(option, arg), option))
		tmp.sort()
		return [i[1] for i in tmp if min(tmp)[0] == i[0]]

	@property
	def options(self):
		return self._options

	@staticmethod
	def lev(a: str, b: str) -> int:
		"""
		levenshtein_distance
		https://en.wikipedia.org/wiki/Levenshtein_distance
		"""
		if len(b) == 0:
			return len(a)
		elif len(a) == 0:
			return len(b)
		elif a[0] == b[0]:
			return OptionsMatcher.lev(a[1:], b[1:])
		else:
			return 1 + min(
				OptionsMatcher.lev(a[1:], b),
				OptionsMatcher.lev(a, b[1:]),
				OptionsMatcher.lev(a[1:], b[1:]),
			)


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
		self.typing = False

	def check(self, function: callable) -> set[str]:
		params = ParamChecker.signature(function)
		odd_param = set(params) - set(self.options)
		hits = set(params) & set(self.options)
		wrong_types = self.check_types(hits, params)
		matches = self.match_parameter(odd_param)
		if matches or wrong_types:
			raise UnsupportedParameters(matches, wrong_types, function)
		return hits

	def check_types(self, hits, params):
		"""
		Checks types and returns the params with types that doesn't match
		"""
		if not self.typing:
			return []
		return [
			(param, mytype, self.options[param])
			for param, mytype in filter(lambda x: x[0] in hits, params.items())
			if mytype != self.options[param]
		]

	def match_parameter(self, odd_params):
		my_matches = []
		for odd in odd_params:
			if matches := self.match(odd):
				my_matches.append((odd, matches))
		return my_matches

	@classmethod
	def with_typing(cls, template_function):
		self = cls(template_function)
		self.typing = True
		return self


class UnsupportedParameters(Exception):
	def __init__(self, matches, wrong_types, function):
		msg = ""
		if wrong_types:
			for param, curr_type, corr_type in wrong_types:
				msg += f"* Wrong Type - Parameter {param}\n"
				f"\t it is '{curr_type.__name__}' "
				f"it should be '{corr_type.__name__}'\n"
		if matches:
			for written, match in matches:
				msg += f"* Parameter '{written}' is not supported,"
				"did you mean:\n"
				for suggestion in match:
					msg += f"\t- {suggestion}\n"
		super().__init__(
			f"\nError in the signature of '{function.__name__}'"
			"in {inspect.getsourcefile(function)}\n" + msg
		)

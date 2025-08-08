import pytest

from dicechanics.ParamChecker import ParamChecker, UnsupportedParameters


def SomePrototype(a, b, c):
	pass


def UserInpt(a, b, p):
	pass


def test_basic_prototype():
	matcher = ParamChecker(SomePrototype)
	try:
		assert matcher.check(SomePrototype) == {"a", "b", "c"}
	except UnsupportedParameters:
		pytest.fail("Checker failed on perfect match")


def test_basic_prototype_raise():
	matcher = ParamChecker(SomePrototype)
	with pytest.raises(UnsupportedParameters):
		matcher.check(UserInpt)


def SomeTypedPrototype(a: int, b: float, c: str):
	pass


def UserTypedInpt(a: float, b: str, c: set):
	pass


def test_typed_prototype():
	matcher = ParamChecker.with_typing(SomeTypedPrototype)
	try:
		assert matcher.check(SomeTypedPrototype) == {"a", "b", "c"}
	except UnsupportedParameters:
		pytest.fail("Typed Checker failed on perfect match")


def test_typed_prototype_error():
	matcher = ParamChecker.with_typing(SomeTypedPrototype)
	with pytest.raises(UnsupportedParameters):
		matcher.check(UserTypedInpt)

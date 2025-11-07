from dicechanics.primitives import SortedString


def test_sortedStringIsSorted():
	string = SortedString("abcabc")
	assert string == "aabbcc"


def test_sortedStringSortsOnConcat():
	string = SortedString("g") + "b" + "c"
	assert string == "bcg"


def test_sortedStringSortsOnMultiply():
	string = SortedString("abc") * 3
	assert string == "aaabbbccc"

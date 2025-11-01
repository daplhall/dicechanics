from dicechanics.parser import text_to_faces


def test_parse():
	f = text_to_faces("1,2,3,4,5,6")
	assert list(f.keys()) == [1, 2, 3, 4, 5, 6]
	assert list(f.values()) == [1, 1, 1, 1, 1, 1]


def test_parse_float():
	f = text_to_faces("1.5,2,3.2,4,5,6")
	assert list(f.keys()) == [1.5, 2.0, 3.2, 4.0, 5.0, 6.0]
	assert list(f.values()) == [1, 1, 1, 1, 1, 1]


def test_parse_count():
	f = text_to_faces("1,1,1,2,3,4")
	assert list(f.keys()) == [1, 2, 3, 4]
	assert list(f.values()) == [3, 1, 1, 1]


def test_parse_repeat():
	f = text_to_faces("1:5,6")
	assert list(f.keys()) == [1, 6]
	assert list(f.values()) == [5, 1]


def test_parse_range():
	f = text_to_faces("1..5,6")
	assert list(f.keys()) == [1, 2, 3, 4, 5, 6]
	assert list(f.values()) == [1, 1, 1, 1, 1, 1]


def test_parse_range_repeat():
	f = text_to_faces("1..5:4,6")
	assert list(f.keys()) == [1, 2, 3, 4, 5, 6]
	assert list(f.values()) == [4, 4, 4, 4, 4, 1]

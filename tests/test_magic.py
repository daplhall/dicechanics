import unittest

import dice_unittest

import dicechanics as tts


class TestDiceMagicMethods(dice_unittest.TestCase):
	def test_dice_iterator(self):
		d = tts.d("1..3:2")
		res = [1, 2, 3]
		for i, j in zip(d, res):
			assert i == j

	def test_dice_iterator_complex(self):
		d = tts.d("1..6:2,6,6,6,6,5,5")
		res = [1, 2, 3, 4, 5, 5, 6, 6, 6]
		for i, j in zip(d, res):
			assert i == j

	def test_dice_contains(self):
		d = tts.d(6)
		assert 6 in d

	def test_boolean_dice(self):
		f = tts.d(6)
		g = tts.d(6)
		assert f is not g
		assert g == f

	def test_hashable_dice(self):
		d = tts.d(6)
		f = {"a": d}
		assert f["a"] == d


if __name__ == "__main__":
	unittest.main()

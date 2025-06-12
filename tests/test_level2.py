import unittest

import dice_unittest

import dicechanics as tts


class TestLevel2(dice_unittest.TestCase):
	def setUp(self):
		self.pool = tts.Pool([tts.d6])

	def test_addint(self):
		newpool = self.pool + 1
		assert newpool._bag == [tts.d6, tts.Die([1])]

	def test_addfloat(self):
		newpool = self.pool + 1.5
		assert newpool._bag == [tts.d6, tts.Die([1.5])]

	def test_adddice(self):
		newpool = self.pool + tts.d10
		assert newpool._bag == [tts.d6, tts.d10]


if __name__ == "__main__":
	unittest.main()

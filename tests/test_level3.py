import unittest

import dicechanics as tts
import dice_unittest


class Testlevel3(dice_unittest.TestCase):
	def setUp(self):
		self.pool = tts.Pool([tts.d6])

	def test_addpool(self):
		newpool = self.pool + tts.Pool([tts.d10, tts.d20])
		self.assertSequenceEqual(newpool._bag, [tts.d6, tts.d10, tts.d20])


if __name__ == "__main__":
	unittest.main()

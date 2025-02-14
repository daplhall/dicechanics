import unittest

import TTStatistics as tts
import dice_unittest

class TestDiceMagicMethods(dice_unittest.TestCase):
	def test_dice_iterator(self):
		d6 = tts.d(6)
		self.assertSequenceAlmostEqual(
			d6.cdf, 
			[0.1667, 0.3333, 0.5, 0.6667, 0.8333, 1],
			4
		)

if __name__ == '__main__':
	unittest.main()
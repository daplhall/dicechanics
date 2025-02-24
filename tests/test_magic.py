import unittest

import DiceStatistics as tts
import dice_unittest

class TestDiceMagicMethods(dice_unittest.TestCase):
	def test_dice_iterator(self):
		d = tts.d('1..3:2')
		res = [1,2,3]
		for i,j in zip(d, res):
			self.assertEqual(i,j)

	def test_dice_iterator_complex(self):
		d = tts.d('1..6:2,6,6,6,6,5,5')
		res = [1,2,3,4,5,5,6,6,6]
		for i,j in zip(d, res):
			self.assertEqual(i,j)
			
	def test_dice_contains(self):
		d = tts.d(6)
		self.assertIn(6, d)

if __name__ == '__main__':
	unittest.main()
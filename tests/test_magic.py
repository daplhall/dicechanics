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
	
	def test_boolean_dice(self):
		f = tts.d(6)
		g = tts.d(6)
		self.assertFalse(f is g)
		self.assertTrue(g == f)

	def test_hashable_dice(self):
		d = tts.d(6)
		f = {'a': d}
		self.assertTrue(f['a'] == d)

if __name__ == '__main__':
	unittest.main()
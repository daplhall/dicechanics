import unittest
import numpy as np

import TTStatistics as tts
import dice_unittest

class TestLevel1(dice_unittest.TestCase):
	"""
	d6 can be a standard dice i generate on enter to avoid repeding
	"""
	def test_plus_dice(self):
		d6 = tts.d(6)
		D = d6 + d6
		self.assertSequenceEqual(
			D.f, 
			[2,3,4,5,6,7,8,9,10,11,12]
		)
		self.assertSequenceAlmostEqual(
			D.p,
			[0.0278,0.0556,0.0833,0.1111,0.1389,
				0.1667,0.1389,0.1111,0.0833,0.0556,0.0278],
			4
		)

	def test_plus_differnt(self):
		d6 = tts.d(6)
		dd = tts.d("2,4,6,8,20")
		D = d6 + dd
		self.assertSequenceEqual(
			D.f, 
			[3,4,5,6,7,8,9,10,11,12,13,14,21,22,23,24,25,26]
		)
		self.assertSequenceAlmostEqual(
			D.p,
			[0.0333,0.0333,0.0667,0.0667,0.10,0.10,0.10,0.10,
			0.0667,0.0667,0.0333,0.0333,0.0333,0.0333,
			0.0333,0.0333,0.0333,0.0333],
			4
		)
	
	def test_matmult(self):
		d6 = tts.d(6)
		D = 2@d6
		self.assertSequenceEqual(
			D.f, 
			[2,3,4,5,6,7,8,9,10,11,12]
		)
		self.assertSequenceAlmostEqual(
			D.p,
			[2.78,5.56,8.33,11.11,13.89,
				16.67,13.89,11.11,5.56,2.78],
			2
		)

if __name__ == '__main__':
	unittest.main()
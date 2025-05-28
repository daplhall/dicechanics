
import unittest
import numpy as np

import DiceStatistics as tts
import dice_unittest

class TestLevel4(dice_unittest.TestCase):
	
	def setUp(self):
		d6 = tts.d6
		self.pool = tts.Pool([d6,d6,d6])
		
	def test_perform(self):
		d = self.pool.perform(lambda x, y: x+y)
		self.assertSequenceEqual(
			d.f, 
			[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
		)
		self.assertSequenceEqual(
			d.c,
			[1, 3, 6, 10, 15, 21, 25, 27, 27, 25, 21, 15, 10, 6, 3, 1]
		)

	def test_add_non_selective(self):
		@self.pool
		def new_dice(x,y):
			return x+y
		d = new_dice()
		self.assertSequenceEqual(
			d.f, 
			[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
		)
		self.assertSequenceEqual(
			d.c,
			[1, 3, 6, 10, 15, 21, 25, 27, 27, 25, 21, 15, 10, 6, 3, 1]
		)

	def test_mult_non_selective(self):
		d = self.pool.perform(lambda x, y: x*y)
		self.assertSequenceEqual(
			d.f, 
			[1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30, 32, 36, 40, 45, 48, 50, 54, 60, 64, 72, 75, 80, 90, 96, 100, 108, 120, 125, 144, 150, 180, 216]		)
		self.assertSequenceEqual(
			d.c,
			[1, 3, 3, 6, 3, 9, 7, 3, 6, 15, 6, 6, 9, 9, 15, 3, 1, 12, 3, 12, 6, 3, 9, 3, 3, 12, 1, 9, 3, 3, 6, 3, 3, 3, 6, 1, 3, 3, 3, 1]		)

if __name__ == '__main__':
	unittest.main()
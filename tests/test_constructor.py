import unittest
import numpy as np

import TTStatistics.Dice as tts
import dice_unittest

class TestConstructor(dice_unittest.TestCase):
	def test_construct_number(self):
		d = tts.Dice(5)
		self.assertSequenceEqual(d.f, [1,2,3,4,5])

	def test_construct_Znumber(self):
		d = tts.Zice(5)
		self.assertSequenceEqual(d.f, [0,1,2,3,4,5])
	
	def test_construct_text1(self):
		d = tts.Dice("1,2,3,4,5,6")
		self.assertSequenceEqual(d.f, [1,2,3,4,5,6])

	def test_construct_text2(self):
		d = tts.Dice("1,2,3..6,9")
		self.assertSequenceEqual(d.f, [1,2,3,4,5,6,9])

	def test_construct_text_count(self):
		d = tts.Dice("1,2,3,3,4")
		self.assertSequenceEqual(d.f, [1,2,3,4])
		self.assertSequenceAlmostEqual(d.p, [0.2,0.2,0.4,0.2], 2)
	
	

if __name__ == '__main__':
	unittest.main()
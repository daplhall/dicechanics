import unittest
import numpy as np

import TTStatistics as tts
import dice_unittest

class TestInterface(dice_unittest.TestCase):

	def Test_construct_number(self):
		d = tts.Dice(5)
		self.assertSequenceEqual(d.f, [1,2,3,4,5],
					seq_type = np.ndarray)
	
	def Test_construct_text1(self):
		d = tts.Dice("1,2,3,4,5,6")
		self.assertSequenceEqual(d.f, np.array([1,2,3,4,5,6]),
					seq_type = np.ndarray)
	
	def Test_construct_text2(self):
		d = tts.Dice("1,2,3..6,9")
		self.assertSequenceEqual(d.f, np.array([1,2,3,4,5,6,9]),
					seq_type = np.ndarray)

	def Test_construct_text_count(self):
		d = tts.Dice("1,2,3,3,4")
		self.assertSequenceEqual(d.f, np.array([1,2,3,4]),
					seq_type = np.ndarray)
		self.assertSequenceAlmostEqual(d.p, np.array([0.2,0.2,0.4,0.2]),
					2)
	
	

if __name__ == '__main__':
	unittest.main()
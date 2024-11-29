import unittest
import numpy as np

import TTStatistics as tts
import dice_unittest

class TestInterface(dice_unittest.TestCase):
	def test_plus_int(self):
		d6 = tts.Dice(6)
		d = d6 + 1
		self.assertsequenceequal(d.f, [2,3,4,5,6,7])
	
	def test_plus_int(self):
		d6 = tts.Dice(6)
		D = d6 + d6
		self.assertSequenceEqual(
			D.f, 
			[2,3,4,5,6,7,8,9,10,11,12]
		)
		self.assertSequenceAlmostEqual(
			D.p,
			[0.0278,0.0556,0.0833,0.1111,0.1389,
				0.1667,0.1389,0.1111,0.0556,0.0278],
			4
		)
	
	def test_plus_float(self):
		d6 = tts.Dice(6)
		d = d6 + 0.5
		self.assertsequenceequal(
			d.f, 
			[1.5,2.5,3.5,4.5,5.5,6.5]
		)
	
	def test_mult_int(self):
		d6 = tts.Dice(6)
		d = d6*2
		self.assertsequenceequal(d.f, [2,4,6,8,10,12])

	def test_mult_float(self):
		d6 = tts.Dice(6)
		d = d6*1.5
		self.assertsequenceequal(
			d.f, 
			[1.5, 3.0, 4.5, 6.0, 7.5, 9.0]
		)

	def test_divide_int_roundup(self):
		control = tts.Dice("1,1,2,2,3,3")
		d6 = tts.Dice(6, roundup = True)
		d = d6/2
		self.assertsequenceequal(d.f, np.array([1,2,3]))
		self.assertSequenceAlmostEqual(
			d.f, 
			[0.33,0.33,0.33],
			2
		)

	def test_divide_int(self):
		d6 = tts.Dice(6)
		d = d6/2
		self.assertsequenceequal(d.f,[0,1,2,3])
		self.assertSequenceAlmostEqual(
			d.f, 
			[0.1667, 0.3333,0.3333,0.1667],
			2
		)

	def test_divide_float(self):
		d6 = tts.Dice(6)
		d = d6/1.5
		self.assertSequenceAlmostEqual(
			d.f,
			[0.0, 0.67, 1.33, 2.0, 2.67, 3.33, 4.0]
		)
		self.assertSequenceAlmostEqual(
			d.p,
			[0.1667,0.1667,0.1667,0.1667,0.1667,0.1667]	
		)

	def test_matmult(self):
		d6 = tts.Dice(6)
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
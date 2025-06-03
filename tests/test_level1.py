import unittest
import numpy as np

import DiceStatistics as tts
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

	def test_plus_differnt_2(self):
		d4 = tts.d(4)
		D = tts.Dice([2] + [3]*2 + [4]*3 + [5]*4 + [6]*5 + [7]*6 \
			+ [8]*5 + [9]*4 + [10]*3 + [11]*2+ [12])
		D = d4+D
		self.assertSequenceEqual(
			D.f, 
			[3,4,5,6,7,8,9,10,11,12,13,14,15,16]
		)
		self.assertSequenceAlmostEqual(
			D.p,
			[0.0069, 0.0208, 0.0417, 0.0694, 0.0972, 0.1250, 0.1389,
    			 0.1389, 0.1250, 0.0972, 0.0694, 0.0417, 0.0208, 0.0069],
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
			[0.0278,0.0556,0.0833,0.1111,0.1389,
				0.1667,0.1389,0.1111,0.0833,0.0556,0.0278],
			4
		)

	def test_matmult_multiple(self):
		d6 = tts.d(6)
		D = 4@d6
		self.assertSequenceEqual(
			D.f, 
			range(4,24+1)
		)
		self.assertSequenceAlmostEqual(
			D.p,
			[0.0008,0.0031,0.0077,0.0154,0.0270,0.0432,0.0617,
    			0.0802,0.0965,0.1080,0.1127,0.1080,0.0965,
			0.0802,0.0617,0.0432,0.0270,0.0154,0.0077,0.0031,0.0008],
			4
		)

	def test_matmult_one(self):
		d6 = tts.d(6)
		D = 1@d6
		self.assertSequenceEqual(
			D.f, 
			range(1,6+1)
		)
		self.assertSequenceAlmostEqual(
			D.p,
			[0.1667,0.1667,0.1667,0.1667,0.1667,0.1667],
			4
		)

	def test_matmult_negative(self):
		d6 = tts.d(6)
		D = -4@d6
		self.assertSequenceEqual(
			D.f, 
			range(-24,-3)
		)
		self.assertSequenceAlmostEqual(
			D.p,
			[0.0008,0.0031,0.0077,0.0154,0.0270,0.0432,0.0617,
    			0.0802,0.0965,0.1080,0.1127,0.1080,0.0965,
			0.0802,0.0617,0.0432,0.0270,0.0154,0.0077,0.0031,0.0008],
			4
		)

	def test_greater_than(self):
		d6 = tts.d(6)
		D = d6>d6
		self.assertSequenceEqual(D.f, [0, 1])
		self.assertSequenceAlmostEqual(
			D.p,
			[0.5833, 0.4167],
			4
		)

	def test_greater_equal_than(self):
		d6 = tts.d(6)
		D = d6>=d6
		self.assertSequenceEqual(D.f, [0, 1])
		self.assertSequenceAlmostEqual(
			D.p,
			[0.4167, 0.5833],
			4
		)

	def test_not_equal_than(self):
		d6 = tts.d(6)
		D = d6!=d6
		self.assertSequenceEqual(D.f, [0, 1])
		self.assertSequenceAlmostEqual(
			D.p,
			[0.1667, 0.8333],
			4
		)
		
	def test_equal_than(self):
		d6 = tts.d(6)
		D = d6==d6
		self.assertSequenceEqual(D.f, [0, 1])
		self.assertSequenceAlmostEqual(
			D.p,
			[0.8333, 0.1667],
			4
		)
		
	def test_rmatmul(self):
		d6 = tts.d(6)
		d2 = tts.d(2)
		D = d2@d6
		self.assertSequenceEqual(D.f, [1,2,3,4,5,6,7,8,9,10,11,12])
		self.assertSequenceAlmostEqual(
			D.p,
			[0.0833, 0.0972, 0.1111, 0.1250, 0.1389, 0.1528, 0.0833,
			0.0694, 0.0556, 0.0417, 0.0278, 0.0139],
			4
		)

	def test_rmatmul2(self):
		f = tts.d('1,3,6')
		g = tts.d('4,7,8')
		D = f@g
		self.assertSequenceEqual(
			D.f, 
			[4,7,8,12,15,16,18,19,20,21,22,23,24,27,28,30,31,32,
    			33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48]
		)
		self.assertSequenceAlmostEqual(
			D.p,
			[0.1111,0.1111,0.1111,0.0123,0.0370,0.0370,0.0370,0.0741,
    			0.0370,0.0123,0.0370,0.0370,0.0128,0.0027,0.0027,0.0069,
			0.0137,0.0069,0.0091,0.0274,0.0274,0.0160,0.0274,0.0412,
			0.0302,0.0206,0.0274,0.0279,0.0165,0.0096,0.0091,0.0069,
			0.0027,0.0005],
			4
		)

	def test_rmatmul3(self):
		f = tts.d('0,1')
		g = tts.d('1,2,3')
		D = f@g
		self.assertSequenceEqual(
			D.f, 
			[0,1,2,3]
		)
		self.assertSequenceAlmostEqual(
			D.p,
			[0.5] + [0.1667]*3,
			4
		)


if __name__ == '__main__':
	unittest.main()
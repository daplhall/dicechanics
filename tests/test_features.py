import unittest
import numpy as np

import DiceStatistics as tts
import dice_unittest

class TestDiceFeatures(dice_unittest.TestCase):
	def test_reroll1(self):
		d = tts.d6.reroll(6)
		self.assertSequenceEqual(
			d.f,
			[1,2,3,4,5,6]
		)
		self.assertSequenceAlmostEqual(
			d.p,
			[0.1944, 0.1944, 0.1944, 0.1944, 0.1944, 0.02778],
			4
		)

	def test_reroll2(self):
		g = 2@tts.d6
		d = g.reroll(7)
		self.assertSequenceEqual(
			d.f,
			[2,3,4,5,6,7,8,9,10,11,12]
		)
		self.assertSequenceAlmostEqual(
			d.p,
			[0.0324, 0.0648, 0.0972, 0.1296, 0.1620, 0.0278, 0.1620,
    			 0.1296, 0.0972, 0.0648, 0.0324],
			4
		)

	def test_reroll3(self):
		g = 3@tts.d6
		d = g.reroll(7)
		self.assertSequenceEqual(
			d.f,
			[3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
		)
		self.assertSequenceAlmostEqual(
			d.p,
			[0.0050, 0.0149, 0.0297, 0.0495, 0.0048, 0.1040, 0.1238, 
			0.1337,	0.1337, 0.1238, 0.1040, 0.0743, 0.0495, 0.0297, 
			0.0149, 0.0050],
			4
		)

	def test_reroll_depth(self):
		g = tts.d6
		d = g.reroll(5,6,depth=2)
		self.assertSequenceEqual(
			d.f,
			[1,2,3,4,5,6]
		)
		self.assertSequenceAlmostEqual(
			d.p,
			[0.2407]*4 + [0.0185]*2,
			4
		)

	def test_reroll_depth2(self):
		g = tts.d10
		d = g.reroll(1,4,6,8,10, depth=6)
		self.assertSequenceEqual(
			d.f,
			[1,2,3,4,5,6,7,8,9,10]
		)
		self.assertSequenceAlmostEqual(
			d.p,
			[0.0016] + [0.1984]*2 
			+ [0.0016,0.1984, 0.0016, 0.1984, 0.0016, 0.1984, 0.0016],
			4
		)

	def test_reroll_inf(self):
		g = tts.d10
		d = g.reroll(7,8,9,10, depth = 'inf')
		self.assertSequenceEqual(
			d.f,
			[1,2,3,4,5,6]
		)
		self.assertSequenceAlmostEqual(
			d.p,
			[0.1667]*6,
			4
		)

	def test_count1(self):
		d = tts.d10.count(5,6)
		self.assertSequenceEqual(
			d.f,
			[0,1]
		)
		self.assertSequenceAlmostEqual(
			d.p,
			[0.8, 0.2],
			4
		)

	def test_explode(self):
		d = tts.d6.explode(5,6)
		self.assertSequenceEqual(
			d.f,
			[1,2,3,4,6,7,8,9,10,11,12]
		)
		self.assertSequenceAlmostEqual(
			d.p,
			[0.1667]*4 + [0.0278] + [0.0556]*5 + [0.0278],
			4
		)

	def test_explode_depth(self):
		d = tts.d6.explode(6, depth = 3)
		self.assertSequenceEqual(
			d.f,
			[1,2,3,4,5,7,8,9,10,11,13,14,15,16,17,19,20,21,22,23,24]
		)
		self.assertSequenceAlmostEqual(
			d.p,
			[0.1667]*5 + [0.0278]*5 + [0.0046]*5 + [0.0008]*5,
			4
		)

	def test_explode_depth2(self):
		d = tts.d6.explode(5,6, depth = 2)
		self.assertSequenceEqual(
			d.f,
			[1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18]
		)
		self.assertSequenceAlmostEqual(
			d.p,
			[0.1667]*4 + [0.0278] + [0.0556]*3 + [0.0278] + [0.0046] + [0.0139] + [0.0185]*4 + [0.0139] + [0.0046],
			4
		)
	
	def test_fold_over(self):
		d = tts.d10
		d = d.fold_over(6)
		self.assertSequenceEqual(d.f, [1,2,3,4,5,6])
		self.assertSequenceAlmostEqual(
			d.p,
			[0.1]*5 + [0.5],
			4
		)
		
	def test_fold_over_into(self):
		d = tts.d10
		d = d.fold_over(6,into = 5)
		self.assertSequenceEqual(d.f, [1,2,3,4,5,6])
		self.assertSequenceAlmostEqual(
			d.p,
			[0.1]*4 + [0.5] + [0.1],
			4
		)

	def test_fold_under(self):
		d = tts.d10
		d = d.fold_under(3)
		self.assertSequenceEqual(d.f, [3,4,5,6,7,8,9,10])
		self.assertSequenceAlmostEqual(
			d.p,
			[0.3] + [0.1]*7,
			4
		)

	def test_fold_under_into(self):
		d = tts.d10
		d = d.fold_under(3, into = 4)
		self.assertSequenceEqual(d.f, [3,4,5,6,7,8,9,10])
		self.assertSequenceAlmostEqual(
			d.p,
			[0.1]+ [0.3] + [0.1]*6,
			4
		)

	def test_fold_under_into_0(self):
		d = tts.d10
		d = d.fold_under(3, into = 0)
		self.assertSequenceEqual(d.f, [0,3,4,5,6,7,8,9,10])
		self.assertSequenceAlmostEqual(
			d.p,
			[0.2]+[0.1]+ [0.1] + [0.1]*6,
			4
		)
		
	
class TestPoolFeatures(unittest.TestCase):
	def test_to_string(self):
		pool = tts.Pool([tts.d6, tts.d6])
		self.assertEqual(
			str(pool),
			'Pool([Dice({1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}), Dice({1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1})])'
		)




if __name__ == '__main__':
	unittest.main()
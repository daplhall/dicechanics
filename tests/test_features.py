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


if __name__ == '__main__':
	unittest.main()
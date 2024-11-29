import unittest
from TTStatistics._textparser import *
import dice_unittest

class TestParser(dice_unittest.TestCase):
	def test_parse(self):
		f, p = parse_to_prop("1,2,3,4,5,6")
		self.assertSequenceEqual(f, [1,2,3,4,5,6])
		self.assertSequenceAlmostEqual(
			p, 
			[0.1667, 0.1667, 0.1667, 0.1667, 0.1667, 0.1667],
			4
		)
	def test_parse_float(self):
		f, p = parse_to_prop("1.5,2,3.2,4,5,6")
		self.assertSequenceEqual(f, [1.5,2.0,3.2,4.0,5.0,6.0])
		self.assertSequenceAlmostEqual(
			p, 
			[0.1667, 0.1667, 0.1667, 0.1667, 0.1667, 0.1667],
			4
		)

	def test_parse_count(self):
		f, p = parse_to_prop("1,1,1,2,3,4")
		self.assertSequenceEqual(f, [1,2,3,4])
		self.assertSequenceAlmostEqual(
			p, 
			[0.5, 0.1667, 0.1667],
			4
		)

	def test_parse_repeat(self):
		f, p = parse_to_prop("1:5,6")
		self.assertSequenceEqual(f, [1,6])
		self.assertSequenceAlmostEqual(
			p, 
			[0.8333, 0.1667],
			4
		)

	def test_parse_range(self):
		f, p = parse_to_prop("1..5,6")
		self.assertSequenceEqual(f, [1,2,3,4,5,6])
		self.assertSequenceAlmostEqual(
			p, 
			[0.1667, 0.1667, 0.1667, 0.1667, 0.1667, 0.1667],
			4
		)

	def test_parse_range_repeat(self):
		f, p = parse_to_prop("1..5:4,6")
		self.assertSequenceEqual(f, [1,2,3,4,5,6])
		self.assertSequenceAlmostEqual(
			p, 
			[0.1905, 0.1905, 0.1905, 0.1905, 0.1905, 0.0476],
			4
		)

if __name__ == '__main__':
	unittest.main()
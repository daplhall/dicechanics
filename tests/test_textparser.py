import unittest
import dice_unittest

from DiceStatistics._parser import text_to_faces, faces_to_count

class TestParser(dice_unittest.TestCase):
	def test_parse(self):
		f = text_to_faces("1,2,3,4,5,6")
		f, c= faces_to_count(f)
		self.assertSequenceEqual(f, [1,2,3,4,5,6])
		self.assertSequenceEqual(c, [1,1,1,1,1,1])

	def test_parse_float(self):
		f = text_to_faces("1.5,2,3.2,4,5,6")
		f, c= faces_to_count(f)
		self.assertSequenceEqual(f, [1.5,2.0,3.2,4.0,5.0,6.0])
		self.assertSequenceEqual(c, [1,1,1,1,1,1])
		

	def test_parse_count(self):
		f = text_to_faces("1,1,1,2,3,4")
		f, c= faces_to_count(f)
		self.assertSequenceEqual(f, [1,2,3,4])
		self.assertSequenceEqual(c, [3,1,1,1])

	def test_parse_repeat(self):
		f = text_to_faces("1:5,6")
		f, c= faces_to_count(f)
		self.assertSequenceEqual(f, [1,6])
		self.assertSequenceEqual(c, [5,1])

	def test_parse_range(self):
		f = text_to_faces("1..5,6")
		f, c= faces_to_count(f)
		self.assertSequenceEqual(f, [1,2,3,4,5,6])
		self.assertSequenceEqual(c, [1,1,1,1,1,1])

	def test_parse_range_repeat(self):
		f = text_to_faces("1..5:4,6")
		f, c = faces_to_count(f)
		self.assertSequenceEqual(f, [1,2,3,4,5,6])
		self.assertSequenceEqual(c, [4,4,4,4,4,1])

if __name__ == '__main__':
	unittest.main()
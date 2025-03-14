import unittest

from DiceStatistics._math import gcd
import dice_unittest

class TestLevel1(dice_unittest.TestCase):
	def test_GCD(self):
		X = [15,10,20,25]
		r = gcd(X[0], X[1])
		for i in X[2:]:
			r = gcd(r, i)
		self.assertEqual(r, 5)

if __name__ == '__main__':
	unittest.main()
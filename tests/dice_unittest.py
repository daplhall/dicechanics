import unittest


class TestCase(unittest.TestCase):
	def assertSequenceAlmostEqual(self, s1, s2, decimal):
		for i, j in zip(s1, s2):
			self.assertAlmostEqual(i, j, decimal)  # noqa: PT009

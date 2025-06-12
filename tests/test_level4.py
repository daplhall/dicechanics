import unittest

import dice_unittest

import dicechanics as tts


class TestNonSelective(dice_unittest.TestCase):
	def setUp(self):
		d6 = tts.d6
		self.pool = tts.Pool([d6, d6, d6])

	def test_perform(self):
		d = self.pool.perform(lambda x, y: x + y)
		assert d.f == [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
		assert d.c == [1, 3, 6, 10, 15, 21, 25, 27, 27, 25, 21, 15, 10, 6, 3, 1]

	def test_add_non_selective(self):
		@self.pool
		def new_dice(x, y):
			return x + y

		d = new_dice()
		assert d.f == [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
		assert d.c == [1, 3, 6, 10, 15, 21, 25, 27, 27, 25, 21, 15, 10, 6, 3, 1]

	def test_mult_non_selective(self):
		d = self.pool.perform(lambda x, y: x * y)
		assert d.f == [
			1,
			2,
			3,
			4,
			5,
			6,
			8,
			9,
			10,
			12,
			15,
			16,
			18,
			20,
			24,
			25,
			27,
			30,
			32,
			36,
			40,
			45,
			48,
			50,
			54,
			60,
			64,
			72,
			75,
			80,
			90,
			96,
			100,
			108,
			120,
			125,
			144,
			150,
			180,
			216,
		]
		assert d.c == [
			1,
			3,
			3,
			6,
			3,
			9,
			7,
			3,
			6,
			15,
			6,
			6,
			9,
			9,
			15,
			3,
			1,
			12,
			3,
			12,
			6,
			3,
			9,
			3,
			3,
			12,
			1,
			9,
			3,
			3,
			6,
			3,
			3,
			3,
			6,
			1,
			3,
			3,
			3,
			1,
		]

	def test_max_non_selective(self):
		d = self.pool.perform(max)
		assert d.f == [1, 2, 3, 4, 5, 6]
		assert d.c == [1, 7, 19, 37, 61, 91]

	def test_min_non_selective(self):
		d = self.pool.perform(min)
		assert d.f == [1, 2, 3, 4, 5, 6]
		assert d.c == [1, 7, 19, 37, 61, 91][::-1]


class TestSelective(dice_unittest.TestCase):
	def test_add_3d6_selective(self):
		d6 = tts.d6
		pool = tts.Pool([d6, d6, d6])
		pool = pool[0, 1, 1]
		d = pool.perform(lambda x, y: x + y)
		assert d.f == list(range(2, 13))
		self.assertSequenceAlmostEqual(
			d.p,
			[
				0.00462962962963,
				0.0138888888889,
				0.0324074074074,
				0.0555555555556,
				0.087962962963,
				0.125,
				0.157407407407,
				0.166666666667,
				0.157407407407,
				0.125,
				0.0740740740741,
			],
			4,
		)

	def test_add_middle_mixed(self):
		pool = tts.Pool([tts.d4, tts.d6, tts.d8])
		d = pool[0, 1, 0].perform(lambda x, y: x + y)
		assert d.f == [1, 2, 3, 4, 5, 6]
		assert d.c == [4, 10, 13, 13, 5, 3]

	def test_add_with_numbers(self):
		pool = tts.Pool([tts.d4, 3])
		d = pool[0, 1].perform(sum)
		assert d.f == [3, 4]
		assert d.c == [3, 1]


if __name__ == "__main__":
	unittest.main()

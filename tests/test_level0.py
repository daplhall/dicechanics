import unittest

import dice_unittest

import dicechanics as tts


class TestLevel0_Dice(dice_unittest.TestCase):
	"""
	d6 can be a standard dice i generate on enter to avoid repeding
	"""

	def test_plus_int(self):
		d6 = tts.d(6)
		d = d6 + 1
		assert d.f == [2, 3, 4, 5, 6, 7]

	def test_plus_float(self):
		d6 = tts.d(6)
		d = d6 + 0.5
		assert d.f == [1.5, 2.5, 3.5, 4.5, 5.5, 6.5]

	def test_sub_int(self):
		d6 = tts.d(6)
		d = d6 - 1
		assert d.f == [0, 1, 2, 3, 4, 5]

	def test_rsub_int(self):
		d6 = tts.d(6)
		d = 1 - d6
		assert d.f == [-5, -4, -3, -2, -1, 0]

	def test_mult_int(self):
		d6 = tts.d(6)
		d = d6 * 2
		assert d.f == [2, 4, 6, 8, 10, 12]

	def test_mult_float(self):
		d6 = tts.d(6)
		d = d6 * 1.5
		assert d.f == [1.5, 3.0, 4.5, 6.0, 7.5, 9.0]

	def test_divide_int(self):
		control = tts.d("0.5, 1.0, 1.5, 2.0, 2.5, 3.0")
		d6 = tts.d(6)
		d = d6 / 2
		assert d.f == control.f
		self.assertSequenceAlmostEqual(d.p, control.p, 2)

	def test_divide_int_roundup(self):
		control = tts.d("1,1,2,2,3,3")
		d6 = tts.d(6, rounding=tts.ops.ceil)
		d = d6 / 2
		assert d.f == control.f
		self.assertSequenceAlmostEqual(d.p, control.p, 2)

	def test_divide_int_rounddown(self):
		d6 = tts.d(6, rounding=tts.ops.floor)
		d = d6 / 2
		assert d.f == [0, 1, 2, 3]
		self.assertSequenceAlmostEqual(d.p, [0.1667, 0.3333, 0.3333, 0.1667], 4)

	def test_divide_int_floor(self):
		d6 = tts.d(6)
		d = d6 // 2
		assert d.f == [0, 1, 2, 3]
		self.assertSequenceAlmostEqual(d.p, [0.1667, 0.3333, 0.3333, 0.1667], 4)

	def test_divide_float(self):
		d6 = tts.d(6)
		d = d6 / 1.5
		self.assertSequenceAlmostEqual(
			d.f, [0.67, 1.33, 2.0, 2.67, 3.33, 4.0], 2
		)
		self.assertSequenceAlmostEqual(
			d.p, [0.1667, 0.1667, 0.1667, 0.1667, 0.1667, 0.1667], 4
		)

	def test_neg(self):
		d6 = tts.d(6)
		g = -d6
		assert g.f == [-6, -5, -4, -3, -2, -1]
		assert g.c == d6.c

	def test_pos(self):
		d6 = tts.d(6)
		g = +d6
		assert g.f == [1, 2, 3, 4, 5, 6]
		assert g.c == d6.c

	def test_greater_than(self):
		d10 = tts.d(10)
		d = d10 > 8
		assert d.f == [0, 1]
		self.assertSequenceAlmostEqual(d.p, [0.8, 0.2], 2)

	def test_greater_eqaual_than(self):
		d10 = tts.d(10)
		d = d10 >= 8
		assert d.f == [0, 1]
		self.assertSequenceAlmostEqual(d.p, [0.7, 0.3], 2)

	def test_less_than(self):
		d10 = tts.d(10)
		d = d10 < 3
		assert d.f == [0, 1]
		self.assertSequenceAlmostEqual(d.p, [0.8, 0.2], 2)

	def test_less_equal_than(self):
		d10 = tts.d(10)
		d = d10 <= 3
		assert d.f == [0, 1]
		self.assertSequenceAlmostEqual(d.p, [0.7, 0.3], 2)
		self.assertSequenceAlmostEqual(d.c, [7, 3], 2)

	def test_not_equal(self):
		d10 = tts.d(10)
		d = d10 != 9
		assert d.f == [0, 1]
		self.assertSequenceAlmostEqual(d.p, [0.1, 0.9], 2)
		self.assertSequenceAlmostEqual(d.c, [1, 9], 2)

	def test_equal(self):
		d10 = tts.d(10)
		d = d10 == 9
		assert d.f == [0, 1]
		self.assertSequenceAlmostEqual(d.p, [0.9, 0.1], 2)
		self.assertSequenceAlmostEqual(d.c, [9, 1], 2)


if __name__ == "__main__":
	unittest.main()

import unittest
import TTStatistics as tts

from anydicefetcher import anydice

class TestDice(unittest.TestCase):
    def test_d6(self):
        """
            testing the values of 1d6
        """
        dice = anydice("""
            output 1d6 named "data"
        """)["data"]
        for i,j in zip(tts.d6.prop, dice["prop"]):
            with self.subTest("Prop", i=i, j=j):
                self.assertAlmostEqual(i,j, places = 12)
        self.assertCountEqual(tts.d6.values, dice["values"]) 
    
    def test_2d6(self):
        """
            testing the values of 2d6 
        """
        dice = anydice("""
            output 2d6 named "data"
        """)["data"]
        my2d6 = 2@tts.d6
        for i,j in zip(my2d6.prop, dice["prop"]):## TODO make a test an assert for this dice tester
            with self.subTest("Prop", i=i, j=j):
                self.assertAlmostEqual(i,j, places = 12)
        self.assertCountEqual(my2d6.values, dice["values"]) 

if __name__ == '__main__':
    unittest.main()
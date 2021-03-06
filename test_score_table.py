from score_table import ScoreTable
import unittest
import shelve
import copy


class TestScoreTable(unittest.TestCase):
    def setUp(self):
        self.path = "score_testing.txt"
        self.score_table = ScoreTable(self.path)

    def testUpdateScore(self):
        self.score_table.scores = []
        self.score_table.update_score(40, "ONE")
        self.score_table.update_score(10, "FOU")
        self.score_table.update_score(20, "TWO")
        self.score_table.update_score(30, "THR")
        expected = [("ONE", 40), ("THR", 30), ("TWO", 20), ("FOU", 10)]
        actual = self.score_table.scores
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
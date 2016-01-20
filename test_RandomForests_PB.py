import unittest, sys
from Bio.RandomForests import RandomForestRegressor
from Bio.RandomForests import RandomForestClassifier

class RandomForestsTest(unittest.TestCase):

    def setUp(self):
        self.X = [[0, 1, "a"], [2, 3, "b"], [4, 5, "a"]]
        self.yw = [0, 1, 2]
        self.y = [0, 1, 0]

    def test_wrong_dimensions(self):

        rfc = RandomForestClassifier.RandomForestClassifier(1)
        rfr = RandomForestRegressor.RandomForestRegressor(1)

        # dimensions not matching
        self.assertRaises(ValueError, rfc.fit, self.X, self.yw[:-1])
        self.assertRaises(ValueError, rfr.fit, self.X, self.yw[:-1])

        # more than two classes in classification task
        self.assertRaises(ValueError, rfc.fit, self.X, self.yw)

        rfc.fit(self.X, self.y)
        rfr.fit(self.X, self.y)

        # not enough data fields
        self.assertRaises(ValueError, rfc.predict, [self.X[0], self.X[1][:2]])
        self.assertRaises(ValueError, rfc.predict_proba, [self.X[0], self.X[1][:2]])
        self.assertRaises(ValueError, rfr.predict, [self.X[0], self.X[1][:2]])

    def test_wrong_values(self):

        rfc = RandomForestClassifier.RandomForestClassifier(1)
        rfr = RandomForestRegressor.RandomForestRegressor(1)

        rfc.fit(self.X, self.y)
        rfr.fit(self.X, self.y)

        # categorical instead of numerical
        self.assertRaises(ValueError, rfc.predict, [[0, "a", "a"]])
        self.assertRaises(ValueError, rfc.predict_proba, [[0, "a", "a"]])
        self.assertRaises(ValueError, rfr.predict, [[0, "a", "a"]])

        # non-numerical values in regression
        self.assertRaises(ValueError, rfr.fit, self.X, [0, 1, "a"])

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)

import unittest

import rss
import gini
import leaf
import node
import randomforestclassifier
import tree

class RandomForestTest(unittest.TestCase):
    
    def test_input(self):
        with self.assertRaises(Exception):
            klasyfikator = randomforestclassifier.RandomForestClassifier(3)
            kl = klasyfikator.fit("Data\gini_testset.txt", "gini_klasyfikacje.txt")
            
        
    def test_empty_input(self):
        with self.assertRaises(IOError):
            klasyfikator = randomforestclassifier.RandomForestClassifier(10)
            kl = klasyfikator.fit("", "gini_klasyfikacje.txt")  
            
    def test_gini_val(self):
        
        X_list, y_list = read_data_class()
        
        gini_val = 0.0
        gini_test = gini.gini(X_list,y_list,3)[2]
        
        self.assertEqual(gini_val, gini_test)
              
    def test_rss(self):
        
        X_list = []
        f = open("regd.txt", "r")
        for i in f:
            X_list.append(i.strip().split("\t"))
        f.close()
        
        y_list = []
        g = open("regkl.txt", "r")
        for j in g:
            y_list.append(float(j.strip()))
        g.close()
        
        rss_val = 1926.0449999999996
        rss_test = rss.rss(X_list,y_list,4)[2]
        
        self.assertEqual(rss_val, rss_test)

    def test_predict(self):
        X,y = read_data_class()
        with self.assertRaises(ValueError):
            RFC = randomforestclassifier.RandomForestClassifier(3)
            RFC.predict(X)
     
    def test_fit(self):
        X,y = read_data_class()
        y = [1,2,3,1,2,3]
        
        with self.assertRaises(TypeError):
            RFC = randomforestclassifier.RandomForestClassifier(3)
            RFC.fit(X,y)

    def test_plant(self):
        X,y = read_data_class()
        with self.assertRaises(ValueError):
            treet = tree.Tree("kl", X, y)

     
def read_data_class():
    X_list = []
    f = open("Data\gini_testset.txt", "r")
    for i in f:
        X_list.append(i.strip().split())
    f.close()
    
    y_list = []
    g = open("Data\gini_klasyfikacje.txt", "r")
    for j in g:
        y_list.append(j.strip())
    g.close()
    
    return X_list, y_list
    
        
if __name__ == '__main__':
    unittest.main()        

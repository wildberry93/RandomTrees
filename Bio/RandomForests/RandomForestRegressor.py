# -*- coding: UTF-8 -*-
import gini
import leaf
import random
import tree
           
class RandomForestRegressor:
    """
    Glowna klasa regresji.
    """
    def __init__(self, num):
        self.num = num
        """Poczatkowa liczba drzew do zbudowania"""
        self.trees = []
        """Lista drzew w lesie"""
        self.ylen = None
        """Długosc wektora y"""
        self.xlen = None
        """Liczba cech w tabeli X"""
        self.typepattern = None
        """Rodzaje typow w danych kolumnach w tabeli"""
        
    def fit(self, X, y, numtrees = 10):
        """
        Input:
        X - macierz z przykladami
        y - wektor z decyzjami
        numtrees - liczba tworzonych drzew
        
        Uczy regresor na zbiorze treningowym X (y jest wektorem, ktory dla 
        kazdego wiersza X zawiera klase, do ktorej nalezy ten przyklad).
        
        Regresor tworzy liczbe drzew wskazana przez uzytkownika.
        """
        RandomForestRegressor.__init__(self, self.num)
        
        self.typepattern = [type(i) for i in X[0]]        

        
        for i in y:
            if type(i) == str:
                raise ValueError("Zmienna y zawiera wartosci nienumeryczne")
        
        if len(X) != len(y):
                raise ValueError("Pierwszy wymiar X i dlugosc y nie sa rowne")
                
        self.xlen = len(X[0])
        self.ylen == len(y)
        
        examples_cnt = len(y)
        for i in range(numtrees):
            indices_yes = [0 for i in range(examples_cnt)]
            indices_no = [0 for i in range(examples_cnt)]
        
            for i in range(examples_cnt):
                new_id = random.randint(0,examples_cnt-1)
                indices_yes[new_id] += 1
                
            for j in range(len(indices_yes)):
                if indices_yes[j] > 0:
                    indices_no[j] = 1
             
            X_yes, y_yes = tree.Tree.examples(X, y, indices_yes)
            X_no, y_no = tree.Tree.examples(X, y, indices_no)
            
            new_tree = tree.Tree("reg", X_yes, y_yes, self.num)
            self.trees.append(new_tree)  
                    
        return self.trees, X
        
    def predict(self, X):
        """
        Wyznacza usredniona wartosc zmiennej zaleznej 
        w oparciu o wszystkie nauczone drzewa w lesie. 
        """
        
        if self.trees == None:
            raise ValueError("Klasyfikator nie zostal nauczony metoda fit")
        
        for i in X:
            if self.xlen != len(i):
                raise ValueError("Nieprawidlowa liczba cech w tabeli X")
            types = [type(j) for j in i]
            if types != self.typepattern:
                raise ValueError("Typy w tabeli X nie zgadzaja sie")
            
        m = []
        
        for przyklad in X:
            decyzje = []
            for t in self.trees:
                decyzje.append(RandomForestRegressor.get_classification(przyklad, t.root))
            m.append(float(sum(decyzje))/len(decyzje))
        return m
            
        
    @staticmethod
    def get_classification(record, node):
        """
        Input:
        record - przyklad do zaklasyfikowania
        node - aktualnie analizowany wierzcholek
        
        Glowna funkcja klasyfikujaca. Rekursyjnie przechodzi po drzewie,
        sprawdzajac klasyfikacje w kolejnych wierzcholkach. 
        
        Zwraca wartosc zmiennej zaleznej dla jednego drzewa i jednego przykladu.
        """
        
        if node.isLeaf():
            return node.results
      
        if node.tb.isLeaf() and node.fb.isLeaf():
            try:
                node.value = float(node.value)
            except:
                pass
                
            if type(node.value) == float or type(node.value) == int:
                if float(record[node.index]) <= float(node.value):
                    return node.tb.results
                else:
                    return node.fb.results 
                    
            elif type(node.value) == str:
                if record[node.index] == node.value:
                    return node.tb.results
                else:
                    return node.fb.results 
        else:
            for i in range(0,len(record)):
                if i == node.index:
                    try:
                        record[i] = float(record[i])
                    except:
                        pass
                    if isinstance(record[i], float):
                        if float(record[i]) <= float(node.value):
                            return RandomForestRegressor.get_classification(record, node.tb)
                        else:
                            return RandomForestRegressor.get_classification(record, node.fb)
                            
                    else:
                        if record[i] == node.value:
                            return RandomForestRegressor.get_classification(record, node.tb)
                        else:
                            return RandomForestRegressor.get_classification(record, node.fb)
                else:
                    continue 

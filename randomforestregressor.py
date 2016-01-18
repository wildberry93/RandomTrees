# -*- coding: UTF-8 -*-
import collections
import gini
import leaf
import random
import tree
           
class RandomForestRegressor:
    """
    Głowna klasa regresji.
    """
    def __init__(self, num):
        self.num = num
        """Poczatkowa liczba drzew do zbudowania"""
        self.trees = []
        """Lista drzew w lesie"""
        self.ylen = None
        self.xlen = None
        
    def fit(self, X, y, numtrees = 15):
        """
        Input:
        X - macierz z przykladami
        y - wektor z decyzjami
        numtrees - liczba poczartkowych drzew
        
        Uczy regresor na zbiorze treningowym X (y jest wektorem, który dla 
        każdego wiersza X zawiera klasę, do której należy ten przykład).
        
        Warunkiem zakończenia procesu uczenia nowych drzew  w lesie
        jest zaobserwowana stabilizacja tzw. błędu out-of-bag (OOB).
        """    
        X_list, y_list = RandomForestRegressor.read_data(X, y) 
        
        # Błędy
        if len(X_list) != len(y_list):
                raise ValueError("Pierwszy wymiar X i długość y nie są równe")
                
        self.xlen = len(X_list[0])
        self.ylen == len(y_list)
        
        for i in range(numtrees):    
            new_tree = tree.Tree("reg", X_list, y_list, self.num)
            self.trees.append(new_tree)  
                    
        return new_tree, X_list
        
    def predict(self, X, isfile=True):
        """
        Przewiduje najbardziej prawdopodobną klasę dla zadanego 
        przykladu dla wszystkich dzrew w lesie. 
        """
        
        # Błędy
        if self.trees == None:
            raise ValueError("Klasyfikator nie został nauczony metodą fit")
        
        if self.xlen != len(X[0]):
            raise ValueError("Nieprawidłowa liczba cech w tabeli X")
            
        m = []
        
        if isfile:
            X_list = []
            f = open(X, "r")
            for i in f:
                X_list.append(i.strip().split("\t"))
            f.close()
            
        if not isfile:
            X_list = X
        
        for przyklad in X_list:
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
        
        Zwraca klase dla jednego drzewa i jednego przykladu.
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

    @staticmethod   
    def read_data(Xfile, yfile):
        """
        Input:
        Xfile - plik z przykładami do uczenia
        yfile - plik z wektorem decyzji
        
        Czyta dane podane przez użytkownika w pliku tekstowym.      
        """
        
        # Pobranie listy przykładów
        X_list = []
        f = open(Xfile, "r")
        for i in f:
            X_list.append(i.strip().split("\t"))
        f.close()
        
        # Pobieranie klasyfikacji
        y_list = []
        g = open(yfile, "r")
        for j in g:
            try:
                y_list.append(float(j.strip()))
            except:
                raise ValueError("Zmienna y zawiera wartości nienumeryczne")
        g.close()
        return X_list, y_list

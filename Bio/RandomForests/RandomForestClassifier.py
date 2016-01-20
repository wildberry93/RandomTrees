# -*- coding: UTF-8 -*-
import gini
import leaf
import node
import random
import tree
           
class RandomForestClassifier:
    """
    Glowna klasa klasyfikacji.  
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
        self.mappings = None
        """Slownik 0 i 1 na klasy wystepujace w danych"""
        self.typepattern = None
        """Rodzaje typow w danych kolumnach w tabeli"""
        
    def fit(self, X, y):   
        """
        Input:
        X - macierz z przykladami
        y - wektor z decyzjami
        
        Uczy klasyfikator na zbiorze treningowym X (y jest wektorem, ktory dla 
        kazdego wiersza X zawiera klase, do ktorej nalezy ten przyklad).
        
        Warunkiem zakonczenia procesu uczenia nowych drzew  w lesie
        jest zaobserwowana stabilizacja tzw. bledu out-of-bag (OOB).
        """  
   
        RandomForestClassifier.__init__(self, self.num)
        
        if len(X) != len(y):
                raise ValueError("Pierwszy wymiar X i dlugosc y nie sa rowne")
        if len(set(y)) > 2:
                raise ValueError("Wektor y zawiera wiecej niz 2 klasy")
                
        self.typepattern = [type(i) for i in X[0]]        
                
        self.xlen = len(X[0])
        self.ylen == len(y)
        
        nowy_y = []
        wartosci = list(set(y))
        for i in y:
            if i == wartosci[0]:
                nowy_y.append(0)
            else:
                nowy_y.append(1)
        y = nowy_y        
        self.mappings = {0: wartosci[0], 1: wartosci[1]}
                    
        examples_cnt = len(y)
        slownik = {}        
        wartosci = []        
        warunek = 1
        while warunek > 0.01:
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
            
            new_tree = tree.Tree("kl", X, y, self.num)
            self.trees.append(new_tree)
            
            for num, index in enumerate(indices_no):
                if index == 1:
                    if num not in slownik:
                        slownik[num]=[]
                    wyniki = []
                    for i in self.trees:
                        wyniki.append(RandomForestClassifier.get_classification(X[num], i.root))
                    if float(sum(wyniki))/len(wyniki) < 0.5:
                        decyzja = 0
                    elif float(sum(wyniki))/len(wyniki) > 0.5:
                        decyzja = 1 
                    elif float(sum(wyniki))/len(wyniki) == 0.5:
                        decyzja = random.randint(0,1)
                             
                    slownik[num].append(decyzja)
             
            wartosci.append(RandomForestClassifier.ooberr(slownik, y))
            
            if len(self.trees) >= 11:
                srednia = float(sum(wartosci[-10:]))/10
                warunek = abs(wartosci[-11] - srednia)    
                    
        return self.trees, wartosci, slownik, X, y
        
        
    @staticmethod
    def get_classification(record, node):
        """
        Input:
        record - przyklad do zaklasyfikowania
        node - aktualnie analizowany wierzcholek
        
        Glowna funkcja klasyfikujaca. Rekurencyjnie przechodzi po drzewie,
        sprawdzajac klasyfikacje w kolejnych wierzcholkach. 
        
        Zwraca klase dla jednego drzewa i jednego przykladu.
        """
        if node.isLeaf():
            return node.results
      
        if node.tb.isLeaf() and node.fb.isLeaf():
            if isinstance(record[node.index], float) or isinstance(record[node.index], int):
                if record[node.index] <= node.value:
                    return node.tb.results
                else:
                    return node.fb.results 
            elif isinstance(record[node.index], str):
                if record[node.index] == node.value:
                    return node.tb.results
                else:
                    return node.fb.results 
           
        else:
            for i in range(0,len(record)):
                if i == node.index:
                    if isinstance(record[i], float) or isinstance(record[i], int):
                        if record[i] <= node.value:
                            return RandomForestClassifier.get_classification(record, node.tb)
                        else:
                            return RandomForestClassifier.get_classification(record, node.fb)
                            
                    elif isinstance(record[i], str):
                        if record[i] == node.value:
                            return RandomForestClassifier.get_classification(record, node.tb)
                        else:
                            return RandomForestClassifier.get_classification(record, node.fb)
                else:
                    continue 
                                    
    def predict(self, X):
        """
        Przewiduje najbardziej prawdopodobna klase dla zadanego 
        przykladu na podstawie decyzji wszystkich drzew w lesie. 
        Zwraca jedna z dwoch mozliwych klas.
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
        X_list = X
        
        for przyklad in X_list:
            decyzje = []
            for t in self.trees:
                decyzje.append(RandomForestClassifier.get_classification(przyklad, t.root))
            
            wspolczynnik = float(sum(decyzje))/len(decyzje)
                        
            if wspolczynnik < 0.5:
                m.append(self.mappings[0])
            elif wspolczynnik > 0.5:
                m.append(self.mappings[1])
            elif wspolczynnik == 0.5:
                r = random.randint(0,1)
                m.append(self.mappings[r])
        
        return m
        
        
    def predict_proba(self, X):
        """
        Input:
        X - lista przykladow
        
        Zwraca wektor prawdopodobienstw (rozmiaru m x 1) 
        przynaleznosci przykladow z X do pierwszej klasy (za pierwsza klase 
        rozumiemy tutaj klase wystepujaca w zbiorze treningowym jako pierwsza) 
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
                decyzje.append(RandomForestClassifier.get_classification(przyklad, t.root))
            wspolczynnik = float(sum(decyzje))/len(decyzje)
            m.append(wspolczynnik)
        return m
                    
    @staticmethod                    
    def ooberr(slownik, y):
        """
        Input:
        slownik - slownik z decyzjami dla kazdego drzewa.
        y - wektor z decyzjami
        
        Funkcja wylicza out-of-bag error na podstawie decyzji dla kazdego drzewa.
        Pomaga zdecydowac o zakonczeniu procesu budowania kolejnych drzew w lesie.
        """
        f_i = 0
        t_i = 0
         
        for przyklad, decyzje in slownik.iteritems():
            for decyzja in decyzje:
                
                if float(y[przyklad]) == decyzja:
                    t_i += 1
                else:
                    f_i += 1

        return float(f_i)/(f_i+t_i)

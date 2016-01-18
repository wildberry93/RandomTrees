import collections
import gini
import leaf
import node
import random
import tree
           
class RandomForestClassifier:
    """
    Glowna klasa budujaca las losowy.  
    """
    def __init__(self, num):
        self.num = num
        """Poczatkowa liczba drzew do zbudowania"""
        self.trees = []
        """Lista drzew w lesie"""
        self.ylen = None
        self.xlen = None
        
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
        
        X_list, y_list = RandomForestClassifier.read_data(X, y)    
   
        if len(X_list) != len(y_list):
                raise ValueError("Pierwszy wymiar X i dlugosc y nie sa rowne")
        if len(set(y_list)) > 2:
                raise ValueError("Wektor y zawiera wiecej niz 2 klasy")
                
        self.xlen = len(X_list[0])
        self.ylen == len(y_list)
                    
        examples_cnt = len(y_list)
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
           
                  
            X_yes, y_yes = RandomForestClassifier.examples(X_list, y_list, indices_yes)
            X_no, y_no = RandomForestClassifier.examples(X_list, y_list, indices_no)
            
            new_tree = tree.Tree("kl", X_yes, y_yes, self.num)
            self.trees.append(new_tree)
            
            for num, index in enumerate(indices_no):
                if index == 1:
                    if num not in slownik:
                        slownik[num]=[]
                    wyniki = []
                    for i in self.trees:
                        wyniki.append(RandomForestClassifier.get_classification(X_list[num], i.root))
                    if float(sum(wyniki))/len(wyniki) < 0.5:
                        decyzja = 0
                    elif float(sum(wyniki))/len(wyniki) > 0.5:
                        decyzja = 1 
                    elif float(sum(wyniki))/len(wyniki) == 0.5:
                        decyzja = random.randint(0,1)
                             
                    slownik[num].append(decyzja)
             
            wartosci.append(RandomForestClassifier.ooberr(slownik, y_list))
            
            if len(self.trees) >= 11:
                srednia = float(sum(wartosci[-10:]))/10
                warunek = abs(wartosci[-11] - srednia)    
                    
        return self.trees, wartosci, slownik, X_list, y_list
        
        
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
            if float(record[node.index]) <= float(node.value):
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
                            return RandomForestClassifier.get_classification(record, node.tb)
                        else:
                            return RandomForestClassifier.get_classification(record, node.fb)
                            
                    else:
                        if record[i] == node.value:
                            return RandomForestClassifier.get_classification(record, node.tb)
                        else:
                            return RandomForestClassifier.get_classification(record, node.fb)
                else:
                    continue 
                    
                    
    def predict(self, X, isfile=True):
        """
        Przewiduje najbardziej prawdopodobna klase dla zadanego 
        przykladu dla wszystkich dzrew w lesie. 
        Zwraca 1 lub 0.
        """
        
        if self.trees == None:
            raise ValueError("Klasyfikator nie zostal nauczony metoda fit")
        
        if self.xlen != len(X[0]):
            raise ValueError("Nieprawidlowa liczba cech w tabeli X")
                 
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
                decyzje.append(RandomForestClassifier.get_classification(przyklad, t.root))
            wspolczynnik = float(sum(decyzje))/len(decyzje)
            if wspolczynnik < 0.5:
                m.append(0)
            elif wspolczynnik > 0.5:
                m.append(1)
            elif wspolczynnik == 0.5:
                m.append(random.randint(0,1))
                
        return m
        
        
    def predict_proba(self, X, isfile=True):
        """
        Input:
        X - lista przykladow
        isfile - czy uzytkownik podal plik czy juz przeczytane dane?
        
        Zwraca wektor (rozmiaru m x 1) prawdopodobienstw 
        przynaleznosci przykladow z X do pierwszej klasy (za pierwsza klase 
        rozumiemy tutaj klase wystepujaca w zbiorze treningowym jako pierwsza) 
        """
        if self.trees == None:
            raise ValueError("Klasyfikator nie zostal nauczony metoda fit")
        
        if self.xlen != len(X[0]):
            raise ValueError("Nieprawidlowa liczba cech w tabeli X")
            
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
        
    @staticmethod    
    def examples(X_list, y_list, indices):
        """
        Input: 
        X_list - lista przykladow
        y_list - lista decyzji
        indices - lista indeksow
        
        Dla zadanych list przykladow X i ich klasyfikacji y oraz listy indeksow 
        indices zwraca przyklady i klasyfikacje pod ustalonymi indeksami.
        """
        X_filtered = []
        y_filtered = []
            
        for i in range(len(indices)):
            if indices[i] > 0:
                for j in range(indices[i]):
                    X_filtered.append(X_list[i])
                    y_filtered.append(y_list[i])
                
        return X_filtered, y_filtered

    @staticmethod    
    def read_data(Xfile, yfile):
        """
        Input:
        Xfile - plik z przykladami do uczenia
        yfile - plik z wektorem decyzji
        
        Czyta dane podane przez uzytkownika w pliku tekstowym.      
        """
        X_list = []
        f = open(Xfile, "r")
        for i in f:
            X_list.append(i.strip().split("\t"))
        f.close()
        
        y_list = []
        g = open(yfile, "r")
        for j in g:
            y_list.append(j.strip())
        g.close()
        return X_list, y_list
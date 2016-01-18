class Node:
    '''
    Klasa Node() reprezentuje pojedynczy wierzcholek w drzewie,
    ktory nie jest lisciem. Kazdy wierzcholek przechowuje
    informacje o wartosci cechy, swoim prawym i lewym synu,
    indeksie cechy oraz wartosci Gini.
    
    Klasa posiada trzy metody: isLeaf(), traverse() oraz liscie().
    '''
    def __init__(self, value=None,tb=None,fb=None,index=None, gn = None):
        self.value=value # value necessary to get a true result
        ''' Wartosc cechy w wierzcholku'''
        self.tb=tb # true decision nodes 
        '''Lewy syn'''
        self.fb=fb # false decision nodes
        '''Prawy syn'''
        self.index = index # feature index
        '''Indeks cechy w wierzcholku'''
        self.gn = gn
        '''Wartosc Gini dla danego wierzcholka'''
        
    def isLeaf(self):
        '''
        Zwraca False jezeli wierzcholek nie jest lisciem.
        '''
        return False




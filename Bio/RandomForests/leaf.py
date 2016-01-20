class Leaf:
    '''
    Klasa Leaf() reprezentuje lisc - ostatni wierzcholek w drzewie,
    ktory przechowuje informacje o klasie.
    '''
    def __init__(self, results):
        self.results = results
        '''
        W przypadku klasyfikacji - jedna z dwoch klas, ktora znajduje sie w lisciu i pozwala
        na podjecie decyzji o klasyfikacji.
	W przypadku regresji - wartosc zmiennej zaleznej.
        '''
    def isLeaf(self):
        '''
        Sprawdza, czy obiekt nalezy do klasy Leaf().
        '''
        return True

class Leaf:
    '''
    Klasa Leaf() reprezentuje lisc - ostatni wierzcholek w drzewie,
    ktory przechowuje informacje o klasie.
    '''
	def __init__(self, results):
		self.results = results
        '''
        Klasa (0 lub 1), ktora znajduje sie w lisciu i pozwala
        na podjecie decyzji o klasyfikacji.
        '''
	def isLeaf(self):
        '''
        Sprawdza, czy obiekt nalezy do klasy Leaf().
        '''
		return True

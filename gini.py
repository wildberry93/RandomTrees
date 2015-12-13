# -*- coding: UTF-8 -*-
import random

def gini(X, y, n_features):
	# Dla zadanej tablicy X zawierającej cechy i ich wartości, tablicy z klasyfikacjami y
	# oraz liczba cech n_features funkcja zwraca krotkę (c, w, g) oznaczające
	# kolejno indeks cechy, wartość oraz wskaźnik Gini impurity. 

	if n_features > len(X[0]):
		raise Exception('Liczba wybranych cech jest większa od liczby cech w zbiorze danych.')

	selected_features = random.sample(xrange(0, len(X[0])), n_features)  # Losowanie cech
			
	all_pairs = [] # Lista zawierająca wszystkie kombinacje (indeks cechy w tabeli, wartość cechy)
	
	for feature in selected_features:
		values = set()
		for wiersz in X:
			value = wiersz[feature]
			if value.isdigit():
				values.add(float(value))
			else:
				values.add(value)
			
		pairs = [(feature, j) for j in values]
		all_pairs.extend(pairs)
	
	# Ustalamy parametry dla wzoru na Gini impurity
	
	def div(x,y): # W przypadku dzielenia, gdy mianownik jest zerem, wartość całego wyrażenia ustalamy na 1
				if y == 0:
					return 1
				return float(x)/float(y)
	
	n = len(all_pairs)
	all_pairs_gini 	= []
	for pair in all_pairs:
		nL, nR, n0L, n1L, n0R, n1R = [0]*6
		for wiersz in range(0, len(X)):
			# Dane kategoryczne
			if type(pair[1]) == str:
				if  pair[1] == X[wiersz][pair[0]]:
					nL += 1
					if float(y[wiersz]) == 0:
						n0L += 1
						
					elif float(y[wiersz]) == 1:
						n1L += 1
				else:
					nR += 1
					if float(y[wiersz]) == 0:
						n0R += 1
						
					elif float(y[wiersz]) == 1:
						n1R += 1
				
			# Dane liczbowe
			if type(pair[1]) == float:
				if  pair[1] <= float(X[wiersz][pair[0]]):
					nL += 1
					if float(y[wiersz]) == 0:
						n0L += 1
						
					elif float(y[wiersz]) == 1:
						n1L += 1
				else:
					nR += 1
					if float(y[wiersz]) == 0:
						n0R += 1
						
					elif float(y[wiersz]) == 1:
						n1R += 1	
			
		gini = div(nL, n) * (div(n0L, nL) * (1 - div(n0L,nL)) + div(n1L, nL) * (1 - div(n1L, nL))) + div(nR, n) * (div(n0R, nR) * (div(n0R, nR)) + div(n1R,nR) * (div(n1R, nR)))
		all_pairs_gini.append(gini)
		
	# Szukamy minimum
	index = min(xrange(len(all_pairs_gini)),key=all_pairs_gini.__getitem__)
				
	return (all_pairs[index][0], all_pairs[index][1], all_pairs_gini[index])
		

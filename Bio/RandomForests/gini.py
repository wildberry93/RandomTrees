# -*- coding: UTF-8 -*-
import random

def gini(X, y, n_features):
        """
        Input:
        X - lista przykladow
        y - wektor decyzji
        n_features - liczba cech
        
        Dla zadanej tablicy X zawierajacej cechy i ich wartosci, tablicy z klasyfikacjami y
        oraz liczba cech n_features funkcja zwraca krotke (c, w, g) oznaczajace
        kolejno indeks cechy, wartosc oraz wskaznik Gini impurity. 
        """
        if n_features > len(X[0]):
                raise Exception('Liczba wybranych cech jest wieksza od liczby cech w zbiorze danych.')

        selected_features = random.sample(xrange(0, len(X[0])), n_features) 
                        
        all_pairs = [] 
        
        for feature in selected_features:
                values = []
                for wiersz in X:
                        value = wiersz[feature]
                        try:
                                value = float(value)
                        except:
                                pass
                        values.append(value)
                pairs = [(feature, j) for j in values]
                all_pairs.extend(pairs)
        
        
        n = len(all_pairs)
        all_pairs_gini  = []
        for pair in all_pairs:
                nL, nR, n0L, n1L, n0R, n1R = [0]*6
                for wiersz in range(0, len(X)):
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
                                
                        if type(pair[1]) == float:
                                if float(X[wiersz][pair[0]]) <= pair[1]:
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

                if nL == 0:
                    nL = 0.01
                if nR == 0:
                    nR = 0.01
                
                def div(x,y):
                        return float(x)/float(y)
                        
                                        
                gini = div(nL, n) * (div(n0L, nL)*(1-div(n0L, nL)) + div(n1L, nL) * (1 - div(n1L, nL))) + div(nR, n) * (div(n0R, nR)*(1-div(n0R, nR)) + div(n1R, nR) * (1 - div(n1R, nR)))
                all_pairs_gini.append(gini)
                
        index = min(xrange(len(all_pairs_gini)),key=all_pairs_gini.__getitem__)
        return (all_pairs[index][0], all_pairs[index][1], all_pairs_gini[index])


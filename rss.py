# -*- coding: UTF-8 -*-
import random

def rss(X, y, n_features):
        """
        Input:
        X - lista przykladow
        y - wektor decyzji
        n_features - liczba cech
        
        Dla zadanej tablicy X zawierajacej cechy i ich wartosci, tablicy z klasyfikacjami y
        oraz liczba cech n_features funkcja zwraca krotke (c, w, g) oznaczajace
        kolejno indeks cechy, wartosc oraz wskaznik RSS. 
        """
        if n_features > len(X[0]):
                raise Exception('Liczba wybranych cech jest wieksza od liczby cech w zbiorze danych.')

        selected_features = random.sample(xrange(0, len(X[0])), n_features)  # Losowanie cech
                        
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
        
        all_pairs_rss  = []
        for pair in all_pairs:
            wyL = []
            l=0
            wyR = []
            r=0
            for wiersz in range(0, len(X)):
                if type(pair[1]) == str:
                    if X[wiersz][pair[0]] == pair[1]:    
                        wyL.append(y[wiersz])
                    else:
                        wyR.append(y[wiersz])
                    
                    
                if type(pair[1]) == float:
                    if float(X[wiersz][pair[0]]) <= pair[1]:    
                        wyL.append(y[wiersz])
                    else:
                        wyR.append(y[wiersz])

            RSS = sum([(i - (sum(wyL)/len(wyL)))**2 for i in wyL]) + sum([(i - (sum(wyR)/len(wyR)))**2 for i in wyR])
            all_pairs_rss.append(RSS)

        index = min(xrange(len(all_pairs_rss)),key=all_pairs_rss.__getitem__)
        return (all_pairs[index][0], all_pairs[index][1], all_pairs_rss[index])

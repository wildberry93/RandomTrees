# -*- coding: UTF-8 -*-
import gini
import random
import node
import leaf
import rss

class Tree:
    """
    Klasa reprezentujaca pojedyncze drzewo w lesie.
    Przechowuje informacje o korzeniu i wywoluje
    rekurencyjna funkcje plantatree(), ktora buduje drzewo.
    """
    def __init__(self, rodzaj, X = None, y = None, num = None):
        if rodzaj == "reg":
            self.root = Tree.plantregg(X, y, num)
        elif rodzaj == "kl":
            self.root = Tree.plantatree(X, y, num)

    @staticmethod
    def plantregg(X, y, num):
        """
        Input:
        X - macierz z przykladami budujacymi drzewo
        y - wektor z decyzjami
        num - liczba cech, sposrod ktorych gini wybiera wartosc podzialu

        Rekurencyjna funkcja budujaca drzewo. Wybiera wartosc podzialu na podstawie
        wlasnosci Gini impurity. Budowanie drzewa konczy sie, kiedy wartosc Gini w wezle
        jest rowna 0.0 - wtedy tez tworzone sa liscie z decyzjami.
        """
        rss_tup = rss.rss(X,y,num)

        set1, set2, y1, y2 = Tree.divideset(X, rss_tup[0], rss_tup[1], y)

        if len(set1) > 3 and len(set2) > 3:
            trueBranch = Tree.plantregg(set1, y1, num)
            falseBranch = Tree.plantregg(set2, y2, num)

            return node.Node(tb=trueBranch, fb=falseBranch, value=rss_tup[1], index=rss_tup[0], gn = rss_tup[2])
        else:
            if len(y1) == 0:
                y1 = y2
            if len(y2) == 0:
                y2 = y1

            y1avg = float(sum(y1))/len(y1)
            y2avg = float(sum(y2))/len(y2)

            return node.Node(tb = leaf.Leaf(y1avg), fb = leaf.Leaf(y2avg), value = rss_tup[1], index=rss_tup[0], gn = rss_tup[2])



    @staticmethod
    def plantatree(X, y, num):
        """
        Input:
        X - macierz z przykladami budujacymi drzewo
        y - wektor z decyzjami
        num - liczba cech, sposrod ktorych gini wybiera wartosc podzialu

        Rekurencyjna funkcja budujaca drzewo. Wybiera wartosc podzialu na podstawie
        wlasnosci Gini impurity. Budowanie drzewa konczy sie, kiedy wartosc Gini w wezle
        jest rowna 0.0 - wtedy tez tworzone sa liscie z decyzjami.
        """
        gini_tup = gini.gini(X,y,num)

        if gini_tup[2] == 0:
            set1, set2, y1, y2 = Tree.divideset(X, gini_tup[0],gini_tup[1],y)

            if len(y1) == 0 and len(y2)>0:
                fbval = float(y2[0])
                tbval = abs(fbval-1)
            elif len(y2) == 0 and len(y1)>0:
                tbval = float(y1[0])
                fbval = abs(tbval-1)
            elif len(y1) > 0 and len(y2) >0:
                tbval = y1[0]
                fbval = y2[0]

            return node.Node(tb=leaf.Leaf(float(tbval)), fb = leaf.Leaf(float(fbval)), value=gini_tup[1], index=gini_tup[0], gn = gini_tup[2])

        else:
            set1, set2, y1, y2 = Tree.divideset(X, gini_tup[0],gini_tup[1],y)

            if len(set1) != 0:
                trueBranch = Tree.plantatree(set1, y1, num)
            else:
                trueBranch = leaf.Leaf(random.randint(0,1))
            if len(set2) != 0:
                falseBranch = Tree.plantatree(set2, y2, num)
            else:
                falseBranch = leaf.Leaf(random.randint(0,1))

            return node.Node(tb=trueBranch, fb=falseBranch, value=gini_tup[1], index=gini_tup[0], gn = gini_tup[2])

    @staticmethod
    def divideset(rows,column,value,y):
        """
        Input:
        rows - lista przykladow
        column - indeks columny z cecha, po ktorej dzielimy
        value - wartosc podzialu
        y - wektor z decyzjami

        Dzieli zbior przykladow na przyklady spelniajace i nie spelniajace
        wartosci w wierzcholku. Zwraca liste z przykladami pozytywnymi i odpowiadajacy
        jej wektor y oraz w takiej samej formie kontrprzyklady.
        """
        split_function=None
        if isinstance(value,float) or isinstance(value,int):
            split_function=lambda row:float(row[column]) <= float(value)
        else:
            split_function=lambda row:row[column]==value

       # Divide the X into two sets and return them
        set1 = [row for row in rows if split_function(row)]
        set2 = [row for row in rows if not split_function(row)]

        y1 = [y[id] for id,row in enumerate(rows) if split_function(row)]
        y2 = [y[id] for id,row in enumerate(rows) if not split_function(row)]

        return (set1,set2,y1,y2)



# -*- coding: UTF-8 -*-
import gini

tabela = []
f = open("gini_dane.txt", "r")
for i in f:
	tabela.append(i.strip().split("\t"))
	
y = []
g = open("gini_klasyfikacje.txt", "r")
for j in g:
	y.append(j.strip())

print "Tabela X z wartościami y po prawej stronie:"
for element in zip(tabela, y):
	print (element[0] + [element[1]])
	

print "Wynik działania funkcji na zbiorze danych\n(indeks cechy / wartość cechy / wartość Gini impurity):"
a = gini.gini(tabela, y, 3)
print a

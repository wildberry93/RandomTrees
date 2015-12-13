#!/usr/bin/python

import gini

class Node:
    def __init__(self, val, samples):
        self.left = None
        self.right = None
        self.value = val
        self.samples = samples

class Tree:
    def __init__(self):
        self.root = None

    def add(self, val, samples_true, samples_false):
        if(self.root is None):
            self.root = Node(val, samples_true) #zmienic, zeby root mial wszystkie samples
        else:
            self._add(val, self.root, samples_true, samples_false)

    def _add(self, val, node, samples_true, samples_false):
        """
        Add new nodes: left and right
        """
        
        if(node.left is not None):
            self._add(val, node.left, samples_true, samples_false)
        else:
            print "jestem nonw"
            print val
            node.left = Node(val, samples_true)
            
        if(node.right is not None):
            self._add(val, node.right, samples_true, samples_false)
        else:
            node.right = Node(val, samples_false)

    def printTree(self):
        if(self.root is not None):
            self._printTree(self.root)

    def _printTree(self, node):
        if(node is not None):
            self._printTree(node.left)
            if node.left is not None and node.right is not None:
                print str(node.left.samples) + ' ' + str(node.right.samples)
            self._printTree(node.right)

def read_data():
    tabela = []
    f = open("gini_dane.txt", "r")
    for i in f:
        tabela.append(i.strip().split("\t"))
    
    y = []
    g = open("gini_klasyfikacje.txt", "r")
    
    for j in g:
        y.append(j.strip())
        
    return tabela, y

def get_samples(index,X,value):
    line_cnt = 0
    samples_true = []
    samples_false = []
    for line in X:
        if line[index] == value:
            samples_true.append(line_cnt)
        else:
            samples_false.append(line_cnt)
        line_cnt+=1
        
    return samples_true, samples_false
    
def build_tree(X,y):
    tree = Tree()
    cnt = 0
    while True: 
        
        if cnt < 5:
            gini_tup = gini.gini(X,y,3)
            #print gini_tup
            samples_true, samples_false = get_samples(gini_tup[0],X,gini_tup[1])
            #print samples_false
            tree.add(gini_tup[1],samples_true, samples_false) #
        else:
            break
        
        cnt+=1
        
        tree.printTree()
        
    return tree
            

if __name__ == "__main__":
    X,y = read_data()
    print y
    build_tree(X,y)
    
    
    
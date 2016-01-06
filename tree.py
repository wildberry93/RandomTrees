from collections import defaultdict
import gini
import random

class Node:
    def __init__(self, results=None, value=None,tb=None,fb=None,index=None):
        self.value=value # value necessary to get a true result
        self.results=results # dict of results for a branch, None for everything except endpoints
        self.tb=tb # true decision nodes 
        self.fb=fb # false decision nodes
        self.index = index #column index
        
def divideset(rows,column,value,y):
    split_function=None
    if isinstance(value,float) or isinstance(value,int):
        print "jestem tutaj num"
        split_function=lambda row:float(row[column])>=float(value)
    else:
        print "jestem tutaj nazwa"
        split_function=lambda row:row[column]==value
    
    print "value", value
   # Divide the X into two sets and return them
    set1 = [row for row in rows if split_function(row)] # if split_function(row)
    print "set1", set1
    y1 = [y[id] for id,row in enumerate(rows) if split_function(row)]
    set2 = [row for row in rows if not split_function(row)]
    print "set2", set2
    y2 = [y[id] for id,row in enumerate(rows) if not split_function(row)]

    return (set1,set2,y1,y2)

def uniquecounts(rows, y):
    results={}
    cnt=0
    for row in rows:
        r=y[cnt]
        cnt+=1
        if r not in results: results[r]=0
        results[r]+=1
    return r  
    
def fit(X, y):
    if len(X) == 0: return Node()
    #print X

    gini_tup = gini.gini(X,y,3)
    set1, set2, y1, y2 = divideset(X, gini_tup[0],gini_tup[1],y)
    print "yyyyyyy1",y1
    print "yyyyyyy2",y2
    if gini_tup[2] > 0:
        trueBranch = fit(set1,y1)
        falseBranch = fit(set2,y2)

        return Node(tb=trueBranch, fb=falseBranch, value=gini_tup[1], index=gini_tup[0])
    else:
        #print uniquecounts(X,y)
        return Node(results=uniquecounts(X,y))
        
'''def printtree(tree,indent=''):
    if tree.results is not None:
        print str(tree.results)
    elif tree.results is None and tree.value is not None:
        print 'Column ' + ' : '+str(tree.value)+'? '
        print indent+'True->', 
        printtree(tree.tb,indent+'  ')
        print indent+'False->', 
        printtree(tree.fb,indent+'  ')'''


def predict(records, trees):
    """
    Classify whole dataset.
    """
    res_dict = defaultdict(list)
    for rec_id,record in enumerate(records):
        for tree in trees:
            result = get_classification(record,tree) #classify each record on every tree
            res_dict[rec_id].append(result)
    print res_dict
    return res_dict        
            
def get_classification(record, tree):
    """
    This function recursively traverses the decision tree and returns a
    classification for the given record.
    """
    print "record", record
    if tree.fb is None and tree.tb is None:
        print "skonczylem"
        return tree.results           
    else:
        for i in range(0,len(record)):
            if i == tree.index:
                #print "biahshdgshj"
                if isinstance(record[i], float) or isinstance(record[i], int):
                    if float(record[i]) >= float(tree.value):
                        return get_classification(record, tree.tb)
                    else:
                        return get_classification(record, tree.fb)
                else:
                    if record[i] == tree.value:
                        return get_classification(record, tree.tb)
                    else:
                        return get_classification(record, tree.fb)
                
            else:
                continue
        
def read_data_to_learn():
    tabela = []
    f = open("gini_dane.txt", "r")
    for i in f:
        tabela.append(i.strip().split("\t"))
    
    y = []
    g = open("gini_klasyfikacje.txt", "r")
    
    for j in g:
        y.append(j.strip())
        
    return tabela, y  

def get_random_lines():
    """
    Draws random lines to from dataset to build single tree.
    The number of lines must be equal to the number of lines 
    in the input dataset.
    Returns X and y.
    """
    
    start_X, start_y = read_data_to_learn()
    numb_lines = len(start_y)
    
    new_X = []
    new_y = []
    
    for i in range(0,numb_lines):
        new_id = random.randint(0,numb_lines-1)
        new_X.append(start_X[new_id])
        new_y.append(start_y[new_id])
    
    return new_X, new_y
    
def read_data_to_classify():
    """
    Reads testset file to classify.
    """
    lines = []
    f = open("gini_testset.txt", "r")
    for i in f:
        lines.append(i.strip().split("\t"))
        
    return lines
    
if __name__ == "__main__":
    X,y = get_random_lines()
    #gini_tup = gini.gini(X,y,2)
    tree1 = fit(X,y)
    tree2 = fit(X,y)
    records = read_data_to_classify()
    predict(records, [tree1,tree2])
    
    
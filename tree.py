import gini


class Node:
    def __init__(self, results=None, value=None,tb=None,fb=None):
        self.value=value # vlaue necessary to get a true result
        self.results=results # dict of results for a branch, None for everything except endpoints
        self.tb=tb # true decision nodes 
        self.fb=fb # false decision nodes
        
def divideset(rows,column,value,y):
    split_function=None
    if isinstance(value,int) or isinstance(value,float):
        split_function=lambda row:row[column]>=value
    else:
        split_function=lambda row:row[column]==value
   
   # Divide the X into two sets and return them
    set1 = [row for row in rows if split_function(row)] # if split_function(row)
    y1 = [y[id] for id,row in enumerate(rows) if split_function(row)]
    set2 = [row for row in rows if not split_function(row)]
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
       
    return results  
    
def buildtree(X, y):
    if len(X) == 0: return Node()
    #print X
    gini_tup = gini.gini(X,y,3)
    set1, set2, y1, y2 = divideset(X, gini_tup[0],gini_tup[1],y)
    if gini_tup[2] > 0:
        trueBranch = buildtree(set1,y1)
        falseBranch = buildtree(set2,y2)

        return Node(tb=trueBranch, fb=falseBranch, value=gini_tup[1])
    else:
        #print uniquecounts(X,y)
        return Node(results=uniquecounts(X,y))
        
def printtree(tree,indent=''):
    if tree.results is not None:
        print str(tree.results)
    elif tree.results is None and tree.value is not None:
        print 'Column ' + ' : '+str(tree.value)+'? '
        print indent+'True->', 
        printtree(tree.tb,indent+'  ')
        print indent+'False->', 
        printtree(tree.fb,indent+'  ')
        
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
    
if __name__ == "__main__":
    X,y = read_data()
    gini_tup = gini.gini(X,y,3)
    printtree(buildtree(X,y))
    
    
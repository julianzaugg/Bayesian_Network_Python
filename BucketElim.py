'''
Created on Jan 3, 2012

@author: julianzaugg
'''
import FactorTable

class Bucket(object):
    """
    A bucket holds factor tables and one variable
    """

    def __init__(self, var):
        """
        Create a bucket by identifying the variable it processes
        """
        self.var = var
        self.factors = set()

    def match(self, f):
        """
        Decides if the factor table belongs in this bucket
        (not exclusively though).
        """
        if hasattr(f, 'labels'):
            if not f:
                return True
            vars = f.labels
            for v in vars:
                if v == self.var:
                    return True
            return False
        else:
            return v == self.var

    def put(self, f):
        """
        placeholder
        """
        self.factors.add(f)

class FactorPool(object):
    """
    FactorPool is the collection of factors, organized into "buckets" as per
    Dechter, R. Bucket Elimination: A Unifying Framework for Probabilistic Inference, in
    Uncertainty in Artificial Intelligence, 1998.
    """
    
    def __init__(self, query, bnet):
        """
        Create a pool of factor tables for a query. The query is a set of variables (or one)
        to which joint probabilities will be assigned, e.g. if {"A", "B"} then the factor pool
        will hold the data necessary to compute P(A, B | Evidence).
        Evidence is provided by "instantiating" the corresponding BNode:s in the BN.
        """
        self.buckets = []
        self.query = query
        self.bn = bnet
        for q in query:
            node = self.bn.nodes[q]
            if node.instance is None:
                self.buckets.append(Bucket(q))

    def is_listed(self, alist, name):
        """
        Check if the name is in a string array
        """
        for s in alist:
            if s == name:
                return True
            else:
                return False

    def is_query(self, var):
        """
        Check if the variable name is in the query variable set, that is
        should NOT be "bucketed"
        """
        self.is_listed(self.query, var)

    def add(self, f):
        """
        Add a new factor to the pool of buckets.
        If needed, variables/parameters are used to create new buckets.
        To achieve a reasonable bucket ordering, factors are assumed
        to be added in a "bottom-up" order of the belief network (children first).
        """
        vars = f.labels
        for v in vars:
            if not self.is_query(v):
                found = False
            for b in self.buckets:
                if b.match(v):
                    found = True
                    break
            if not found:
                self.buckets.insert(len(self.buckets) - len(self.query), Bucket(v))
        added = False
        for b in self.buckets:
            if b.match(f):
                added = True
                b.put(f)
                break
        return added

    def is_answer(self):
        """
        Decide on whether we are ready to finish inference.
        """
        return len(self.buckets) <= 1

    def sum_bucket(self):
        if len(self.buckets) > 0:
            b = self.buckets[0]
            prod = None
            self.buckets.pop(0)
            sumvar = b.var
            #if the bucket is a query bucket (involves a query variable),
            #we don't sum-out anything
            if self.is_query(sumvar):
                for curr in b.factors:
                    if prod is not None:
                        prod = prod.product(curr)
                    else:
                        prod = curr
                return prod
            else:
                #the bucket has a variable that needs summing-out
                #we do this in two phases: 
                #phase 1: compute an initial product that needs summing-out
                for curr in b.factors:
                    if self.is_listed(curr.labels, sumvar):
                        if prod is not None:
                            prod = prod.product(curr)
                        else:
                            prod = curr
                #check so that we actually have a factor to sum this 
                #variable from
                if prod is not None:
                    prod = prod.sumout(sumvar)
                #phase 2: compute the full product involving only the factors
                #that were excluded above
                for curr in b.factors:
                    if self.is_listed(curr.labels, sumvar):
                        print
                    else:
                        if prod is not None:
                            prod = prod.product(curr)
                        else:
                            prod = curr
                return prod
        return None


class BucketElim(object):
    '''
    Implementation of _exact_ belief updating in accordance with the method described in  
    Dechter, R. Bucket Elimination: A Unifying Framework for Probabilistic Inference, in
    Uncertainty in Artificial Intelligence, 1998.
    '''
    def __init__(self, bnet):
        '''
        Create an inference session with a particular setting of BN parameters
        (including what variables that are set).
        '''
        self.bn = bnet
        self.log_likelihood = 9999999
        self.evidmap = {}
        self.fpool = FactorPool([], self.bn)
        self.visited = set()
        
    def make_factor(self, nodename, query):
        children = self.bn.get_children(nodename)
        for child in children:
            if child not in self.visited:
                self.visited.add(child)
                self.make_factor(child, query)
        f = None
        #The code below strips out any variables that are instantiated
        curr = self.bn.nodes[nodename]
        for parent in self.bn.get_parents(nodename):
            pnode = self.bn.nodes[parent]
            evid = pnode.instance
            if evid is not None:
                curr = curr.select(parent, evid)
        #add factor for this cpt to the pool
        f = FactorTable(curr)
        self.fpool.add(f)

    def infer(self, query):
        '''
        Perform inference on the Bayesian network.
        Infer the conditional probability of the specified query variables
        GIVEN the current BN, i.e. P(Q1,Q2,...,Qn|BN); where BN is the model
        parameters and the evidence (observations).
        Note that evidence are incorporated into the BN instance
        (e.g. using cpt.setInstance(true)).
        This inference is exact and uses Bucket elimination
        '''
        fpool = FactorPool(query, self.bn)
        #start at roots
        roots =self.bn.get_roots()
        #create a factor pool consisting of all buckets with factor tables
        for node in roots:
            self.visited.add(node.name)
            self.make_factor(node.name, query)
        f = self.fpool.sum_bucket()
        self.fpool.add(f)
        result = []
        while not self.fpool.is_answer():
            f = self.fpool.sum_bucket()
            #if the resulting factor can't be added it means that there 
            #is nothing more we can do about it, it is a result factor
            if not self.fpool.add(f):
                result.append(f)
        prod = None
        for cur in result:
            if prod is None:
                prod = cur
            else:
                prod = prod.product(cur)
        self.log_likelihood = prod.get_log_likelihood()
        return prod.get_jpt(query)



'''
Created on Jan 11, 2012

@author: julianzaugg
'''
#cython: profile=True

try:
    from cBNet import BNet
except ImportError, e:
    print e
    from BNet import BNet
from CPT import CPT
from GDT import GDT

class TrainExample(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def main(self):
        values=[
            #  A      G      F      E      C
            [True,  False, True,  True,   0.1],
            [True,  True,  True,  True,   0.2],
            [True,  False, True,  True,   0.5],
            [False, True,  True,  False, -0.3],
            [True,  False, True,  False, -0.0],
            [True,  True,  True,  False, -0.2],
            [True,  False, False, True,   0.6],
            [False, True,  False, True,   0.8],
            [True,  True,  False, True,   0.1],
            [False, False, False, False, -0.8],
            [False, True,  False, False, -0.2],
            [False, True,  False, False, -0.3],
            [False, True,  False, False, -0.5]]
        # construct a BN with two root nodes
        a = CPT("A", [])
        b = CPT("B", [])
        c = GDT("C",  ["B"]) # Gaussian continuous
        d = CPT("D",  ["A"])
        e = CPT("E",  ["A", "B"])
        f = CPT("F",  ["D", "E"])
        g = CPT("G",  ["F"])
        # put them all into the BN
        bn = BNet()
        bn.add(a)
        bn.add(b)
        bn.add(c)
        bn.add(d)
        bn.add(e)
        bn.add(f)
        bn.add(g)

        # train it using EM
        bn.train( ["A", "G", "F", "E", "C"], values,  ["B", "D"], 9)
        print a
        print b
        print c
        print d
        print e
        print f
        print g

        c.instance = 0.5
        a.instance = True
        test = bn.infer_naive(["E"])
        test.normalize()
        print test

    def main2(self):

        values = [
            #  A      G      F      E      
            [True,  False, True,  True],
            [True,  True,  True,  True],
            [True,  False, True,  True],
            [False, True,  True,  False],
            [True,  False, True,  False],
            [True,  True,  True,  False],
            [True,  False, False, True],
            [False, True,  False, True],
            [True,  True,  False, True],
            [False, False, False, False],    
            [False, True,  False, False],
            [False, True,  False, False],
            [False, True,  False, False]]
        # construct a BN with two root nodes
        a = CPT("A", [])
        b = CPT("B", [])
        d = CPT("D",  ["A"])
        e = CPT("E",  ["A", "B"])
        f = CPT("F",  ["D", "E"])
        g = CPT("G",  ["F"])
        # put them all into the BN
        bn = BNet()
        bn.add(a)
        bn.add(b)
        bn.add(d)
        bn.add(e)
        bn.add(f)
        bn.add(g)

        # train it using EM
        bn.train( ["A", "G", "F", "E"], values,  ["B", "D"], 9)
        print a
        print b
        print d
        print e
        print f
        print g

        a.instance = True
        test = bn.infer_naive(["E"])
        test.normalize()
        print test
        
    def main3(self):
        values=[  
        [-0.1, None],
        [-0.5, None],
        [-0.3, True],
        [0.3, None],
        [0.4, None],
        [0.1, None],
        [-0.4, None],
        [-0.2, None],
        [-0.3, None],
        [0.1, None],
        [0.4, False],
        [0.2, None]
        ]
        # construct a BN with one boolean root and one continuous child
        a= CPT("A", [])
        b= GDT("B", ["A"])
        #b.setTieVariances(True)
        bn= BNet()
        bn.add(a)
        bn.add(b)
        #bn.EM_PRINT_STATUS=True
        # train it using EM
#        bn.train(["B","A"], values, [], 5)
        bn.train(["B"], values, ["A"], 5)
        print a
        print b

        b.instance = 0.0
        test = bn.infer_naive(["A"])
        test.normalize()
        print test
    
    def main4(self):
        values=[
            #  A      G      F      E      C    B    D
            [True,  False, True,  True,   0.1, False, True],
            [True,  True,  True,  True,   0.2, True, True],
            [True,  False, True,  True,   0.5, False, False],
            [False, True,  True,  False, -0.3, False, True],
            [True,  False, True,  False, -0.0, True, True],
            [True,  True,  True,  False, -0.2, False, True],
            [True,  False, False, True,   0.6, False, True],
            [False, True,  False, True,   0.8, False, True],
            [True,  True,  False, True,   0.1, True, True],
            [False, False, False, False, -0.8, True, False],
            [False, True,  False, False, -0.2, False, True],
            [False, True,  False, False, -0.3, True, True],
            [False, True,  False, False, -0.5, False, True]]
        
        a = CPT("A", [])
        b = CPT("B", [])
        c = GDT("C",  ["B"]) # Gaussian continuous
        d = CPT("D",  ["A"])
        e = CPT("E",  ["A", "B"])
        f = CPT("F",  ["D", "E"])
        g = CPT("G",  ["F"])
        # put them all into the BN
        bn = BNet()
        bn.add(a)
        bn.add(b)
        bn.add(c)
        bn.add(d)
        bn.add(e)
        bn.add(f)
        bn.add(g)

        # train it using EM
        bn.train( ["A", "G", "F", "E", "C", "B", "D"], values,  [], 9)
#        bn.train( ["A", "G", "F", "E"], values,  ["B", "D"], 9)
        print a
        print b
        print c
        print d
        print e
        print f
        print g
        
        c.instance = 0.5
        a.instance = True
        test = bn.infer_naive(["E"])
        test.normalize()
        print test
    

if __name__ == '__main__':
#    test = TrainExample()
    TrainExample().main()
#    import timeit
#    temp = timeit.Timer(test.main).timeit(1)
#    print "Time Taken : %.3f seconds" % temp
#    test.main()
    
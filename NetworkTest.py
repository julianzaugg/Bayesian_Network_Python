'''
Created on Jan 24, 2012

@author: julianzaugg
'''
import unittest
from CPT import CPT
from GDT import GDT
from Gaussian import Gaussian
try:
    from cBNet import BNet
except ImportError, e:
    print e
    from BNet import BNet

#Lose prints and add asserts
class Test(unittest.TestCase):

    def setUp(self):
        self.burglary = CPT("B", [])
        self.burglary.put([], 0.001)
        
        self.earthquake = CPT("E", [])
        self.earthquake.put([], 0.002)
        
        self.alarm = CPT("A", ["B", "E"],
                    {
                     (True, True): 0.95,
                     (True, False): 0.94,
                     (False, True): 0.29,
                     (False, False): 0.001
                     }
                    )

        self.johncalls = CPT("J", ["A"], 
                        {
                        (True,): 0.9,
                        (False,): 0.05
                        }
                        )

        self.marycalls = CPT("M", ["A"], 
                        {
                        (True,) : 0.7,
                        (False,) : 0.01
                        }
                        )

        self.bn = BNet()
        self.bn.add(self.burglary)
        self.bn.add(self.earthquake)
        self.bn.add(self.alarm)
        self.bn.add(self.johncalls)
        self.bn.add(self.marycalls)
        
        self.A = CPT("A", [])
        self.A.put([], 0.36)
        
        self.B = CPT("B", [])
        self.B.put([], 0.21)
        
        self.D = CPT("D", ["A"])
        self.D.put([True], 0.12)
        self.D.put([False], 0.84)
        
        self.E = CPT("E", ["A", "B"])
        self.E.put([True, True], 0.76)
        self.E.put([False, True], 0.14)
        self.E.put([True, False], 0.57)
        self.E.put([False, False], 0.68)
        
        self.F = CPT("F", ["D", "E"])
        self.F.put([True, True], 0.06)
        self.F.put([False, True], 0.007)
        self.F.put([True, False], 0.61)
        self.F.put([False, False], 0.061)
        
        self.G = CPT("G", ["F"])
        self.G.put([True], 0.481)
        self.G.put([False], 0.085)
        self.bn_2 = BNet()
        self.bn_2.add(self.A)
        self.bn_2.add(self.B)
        self.bn_2.add(self.D)
        self.bn_2.add(self.E)
        self.bn_2.add(self.F)
        self.bn_2.add(self.G)


    def tearDown(self):
        pass

    def testsimple1(self):
        print "\n****Setting JohnCalls = True and MaryCalls = True****"
        self.johncalls.instance = True
        self.marycalls.instance = True
        test = self.bn.infer_naive(["B"])
        test.normalize()
        print test
        self.assertAlmostEqual(test.get([True]), 0.284, 3)

    def testsimple2(self):
        print "\n****Setting Earthquake = False****"
        self.burglary.instance = None
        self.earthquake.instance = False
        test = self.bn.infer_naive(["B", "E"])
        test.normalize()
        print test

    def testsimple3(self):
        print "\n****Setting burglary = True****"
        self.earthquake.instance = None
        self.burglary.instance = True
        test = self.bn.infer_naive(["B", "E"])
        test.normalize()
        print test

    def testancestors(self):
        print "\n****Checking Ancestors****"
        self.assertEqual(self.bn.get_ancestors("J"), 
                         set(["B", "E", "A"]))
        self.assertEqual(self.bn.get_ancestors("M"), 
                         set(["B", "E", "A"]))
        self.assertEqual(self.bn.get_ancestors("B"), 
                         set([]))
        self.assertEqual(self.bn.get_ancestors("E"), 
                         set([]))

    def testnodevalueget(self):
        print "\n****Checking getting node values****"
        print "Burglary True"
        print self.burglary.get(True, [])
        print "Earthquake False"
        print self.earthquake.get(False, [])
        print "Alarm True, parents True:True"
        print self.alarm.get(True, [True, True])
        print "Alarm True, parents False:True"
        print self.alarm.get(True, [False, True])

    def testroot(self):
        print "\n****Checking node root****"
        self.assertTrue(self.burglary.is_root())
        self.assertFalse(self.alarm.is_root())
        self.assertFalse(self.johncalls.is_root())
        X = CPT("X", ["M"])
        self.assertFalse(X.is_root())

    def testadvanced(self):
        print "\n****Testing inference larger network****"
        print "Setting marycalls = False & burglary = True, inferring X"
        X = CPT("X", ["M"])
        X.put([True], .89)
        X.put([False], .56)

        Y = CPT("Y", ["A", "B"])
        Y.put([True, False], .23)
        Y.put([False, True], .74)
        Y.put([False, False], .57)
        Y.put([True, True], .12)
#
        Z = CPT("Z", ["X", "Y"])
        Z.put([True, True], 0.23)
        Z.put([False, False], 0.41)
        Z.put([True, False], 0.16)
        Z.put([False, True], 0.75)

        self.bn.add(X)
        self.bn.add(Y)
        self.bn.add(Z)
#        print X
#        print Y
#        print Z

        self.marycalls.instance = False
        self.burglary.instance = True
#        for node in self.bn.nodes.values():
#            print node
#            print node.name
#            print node.instance
        test =  self.bn.infer_naive(["X"])
        test.normalize()
        print test
        test2 = self.bn.infer_naive(["Z", "A", "E"])

    def testadvanced2(self):
        print "\n****Testing inference larger network****"
        print "Setting alarm = False & burglary = True, inferring [Z,A,E]"
        
        X = CPT("X", ["M"])
        X.put([True], .89)
        X.put([False], .56)

        Y = CPT("Y", ["A", "B"])
        Y.put([True, False], .23)
        Y.put([False, True], .74)
        Y.put([False, False], .57)
        Y.put([True, True], .12)
#
        Z = CPT("Z", ["X", "Y"])
        Z.put([True, True], 0.23)
        Z.put([False, False], 0.41)
        Z.put([True, False], 0.16)
        Z.put([False, True], 0.75)

        self.bn.add(X)
        self.bn.add(Y)
        self.bn.add(Z)
        
        self.alarm.instance = False
        self.burglary.instance = True
        
        test = self.bn.infer_naive(["Z", "A", "E"])
        test.normalize()
        print test
        
    def testadvanced3(self):
        print "\n****Testing inference larger network****"
        print "Setting alarm = False & Y = True, inferring C"
        
        X = CPT("X", ["M"])
        X.put([True], .89)
        X.put([False], .56)

        Y = CPT("Y", ["A", "B"])
        Y.put([True, False], .23)
        Y.put([False, True], .74)
        Y.put([False, False], .57)
        Y.put([True, True], .12)
#
        Z = CPT("Z", ["X", "Y"])
        Z.put([True, True], 0.23)
        Z.put([False, False], 0.41)
        Z.put([True, False], 0.16)
        Z.put([False, True], 0.75)
        
        C = CPT("C", ["B"])
        C.put([True], .36)
        C.put([False], .67)

        self.bn.add(X)
        self.bn.add(Y)
        self.bn.add(Z)
        self.bn.add(C)
        Y.instance = True
        self.alarm.instance = False
        
        test = self.bn.infer_naive(["C"])
        test.normalize()
        print test
    
    def testadvanced4(self):
        print "\n****Testing inference larger network (Train network)****"
        print "Setting A = True, inferring F"
        self.A.instance = True
        test = self.bn_2.infer_naive(["F"])
        test.normalize()
        print test
    
    def testadvanced5(self):
        print "\n****Testing inference larger network (Train network)****"
        print "Setting A = True, inferring extra C node (not GDT)"
        C = CPT("C", ["B"])
        C.put([True], 0.95)
        C.put([False], 0.86)
        self.bn_2.add(C)
        self.A.instance = True
        test = self.bn_2.infer_naive(["C"])
        test.normalize()
        print test
    
    def testadvanced6(self):
        print "\n****Testing inference larger network (Train network)****"
        print "Setting A = True, inferring extra C node (not GDT) and D,E"
        C = CPT("C", ["B"])
        C.put([True], 0.95)
        C.put([False], 0.86)
        self.bn_2.add(C)
        self.A.instance = True
        test = self.bn_2.infer_naive(["C", "D", "E"])
        test.normalize()
        print test
        
        
    def testrelevant(self):
        print "\n****Testing getting relevant network****"
        print "Getting relevant network for node J in expanded network"
        
        X = CPT("X", ["M"])
        X.put([True], .89)
        X.put([False], .56)

        Y = CPT("Y", ["A", "B"])
        Y.put([True, False], .23)
        Y.put([False, True], .74)
        Y.put([False, False], .57)
        Y.put([True, True], .12)
#
        Z = CPT("Z", ["X", "Y"])
        Z.put([True, True], 0.23)
        Z.put([False, False], 0.41)
        Z.put([True, False], 0.16)
        Z.put([False, True], 0.75)

        self.bn.add(X)
        self.bn.add(Y)
        self.bn.add(Z)
        
        print self.bn.get_relevant("J").nodes.keys()
    
    def test_GDT_advanced(self):
        print "\n****Testing large network inferring GDT****"
        X = CPT("X", ["M"])
        X.put([True], .89)
        X.put([False], .56)

        Y = CPT("Y", ["A", "B"])
        Y.put([True, False], .23)
        Y.put([False, True], .74)
        Y.put([False, False], .57)
        Y.put([True, True], .12)
#
        Z = CPT("Z", ["X", "Y"])
        Z.put([True, True], 0.23)
        Z.put([False, False], 0.41)
        Z.put([True, False], 0.16)
        Z.put([False, True], 0.75)
        
        G  = GDT("G", ["X"])
        G.put(Gaussian(0.24, 0.5), [True])
        G.put(Gaussian(0.62, .1), [False])

        self.bn.add(X)
        self.bn.add(Y)
        self.bn.add(Z)
        self.bn.add(G)
#        print self.bn.get_relevant("G").nodes.keys()
#        print G
        test = self.bn.infer_naive("G")
        print test
        
    def testtrain1(self):
        """
        \n****Testing training the large train network,
        two unknown, one GDT****
        """
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
        
        a = CPT("A", [])
        b = CPT("B", [])
        c = GDT("C",  ["B"]) # Gaussian continuous
        d = CPT("D",  ["A"])
        e = CPT("E",  ["A", "B"])
        f = CPT("F",  ["D", "E"])
        g = CPT("G",  ["F"])
        bn = BNet()
        bn.add(a)
        bn.add(b)
        bn.add(c)
        bn.add(d)
        bn.add(e)
        bn.add(f)
        bn.add(g)
        
        bn.train( ["A", "G", "F", "E", "C"], values,  ["B", "D"], 9)
        c.instance = 0.5
        a.instance = True
        test = bn.infer_naive(["E"])
        test.normalize()
        print test
    
    def  testtrain2(self):
        """
        \n****Testing training the small train network,
        ****
        """
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

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
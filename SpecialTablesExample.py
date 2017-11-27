'''
Created on Feb 15, 2012

@author: julianzaugg
'''
try:
    from BNet import BNet
    from cTable_Utils import entry
except ImportError, e:
    print e
    from BNet import BNet
from CPT import CPT
from GDT import GDT
from Gaussian import Gaussian
from NoisyOR import NoisyOR

class SpecialTablesExample(object):
    '''
    classdocs
    '''
    def test_train(self):
        values=[
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
        
        nor= NoisyOR("or", ["v1","v2","v3","v4"])
        v1= CPT("v1", [])
        v2= CPT("v2", [])
        v3= CPT("v3", [])
        v4= CPT("v4", [])
        y= GDT("y", ["or"])
        bn = BNet()
        bn.add(nor)
        bn.add(v1)
        bn.add(v2)
        bn.add(v3)
        bn.add(v4)
        bn.add(y)
        bn.train(  ["v1","v2","v3","v4","y"], values,   ["or"], 1)
        print nor
        print y
        print v1
        print v2
        print v3
        print v4
        
    def test(self):
        nor = NoisyOR("or", ["v1","v2","v3","v4"])
#        for i in range(16):
#            print entry(i, 4)
        nor.put([True, True, True, True], 0.65)
        nor.put([False, True, True, True], 0.19)
        nor.put([True, False, True, True], 0.48)
        nor.put([False, False, True, True], 0.53)
        nor.put([True, True, False, True], 0.98)
        nor.put([False, True, False, True], 0.68)
        nor.put([True, False, False, True], 0.57)
        nor.put([False, False, False, True], 0.90)
        nor.put([True, True, True, False], 0.43)
        nor.put([False, True, True, False], 0.39)
        nor.put([True, False, True, False], 0.71)
        nor.put([False, False, True, False], 0.34)
        nor.put([True, True, False, False], 0.01)
        nor.put([False, True, False, False], 0.06)
        nor.put([True, False, False, False], 0.92)
        nor.put([False, False, False, False], 0.36)

        v1= CPT("v1", [])
        v1.put([], 0.54)
        v2= CPT("v2", [])
        v2.put([], 0.46)
        v3= CPT("v3", [])
        v3.put([], 0.05)
        v4= CPT("v4", [])
        v4.put([], 0.64)

        y= GDT("y", ["or"])
        y.put(Gaussian(0.51, 0.5), [True])
        y.put(Gaussian(0.61, .1), [False])

#        for i in [v1,v2,v3,v4,y, nor]:
#            print i   
        bn = BNet()
        bn.add(nor)
        bn.add(v1)
        bn.add(v2)
        bn.add(v3)
        bn.add(v4)
        bn.add(y)
        
        test = bn.infer_naive(["or"])
        test.normalize()
        print test

        test = bn.infer_naive(["v1"])
        test.normalize()
        print test

        test = bn.infer_naive(["v2"])
        test.normalize()
        print test

        test = bn.infer_naive(["v3"])
        test.normalize()
        print test

        test = bn.infer_naive(["v4"])
        test.normalize()
        print test
    
    """
    PYTHON VERSION TO BE ADDED
    """
#    public static void main1(String[] args){
#        NoisyOR cpt1=new NoisyOR("fever", new String[] {"cold", "flu", "malaria"});
#        cpt1.put(new Boolean[] {true, false, false}, 0.4);
#        cpt1.put(new Boolean[] {false, true, false}, 0.8);
#        cpt1.put(new Boolean[] {false, false, true}, 0.9);
#        for (String thing: cpt1.getParents()){
#            System.out.print("\t" + thing);
#        }
#        System.out.println("");
#        for (int i = 0; i < 8; i++){
#            Boolean[] temp  = CPT.entry(i, 3);
#            for (int j = 0; j < temp.length; j++){
#                System.out.print("\t");
#                System.out.print(temp[j]);
#            }
#            System.out.print("\t");
#            System.out.print(String.format("%4.2f", cpt1.get(temp, true)));
#            System.out.print("\t");
#            System.out.print(String.format("%4.2f", cpt1.get(temp, false)));
#            System.out.println("");
#            
#            
#        }
#        
#    }

if __name__ == '__main__':
    SpecialTablesExample().test()
    SpecialTablesExample().test_train()

'''
Created on Dec 19, 2011

@author: julianzaugg
'''
from CPT import CPT
from GDT import GDT
from BNet import BNet


class SimpleExample(object):
    '''
    placeholder
    '''
    def __init__(self):
        '''
        placeholder
        '''
        burglary = CPT("B", [], 
                       {
                        ():0.001
                        }
                       )
#        burglary.put([], 0.001)
#        burglary.put(
#                     {
#                      (): 0.001
#                      }
#                     )
#        print burglary

        earthquake = CPT("E", [],
                         {
                          ():0.002
                          }
                         )
#        earthquake.put([], 0.002)
#        print earthquake

        alarm = CPT("A", ["B", "E"],
                    {
                     (True, True): 0.95,
                     (True, False): 0.94,
                     (False, True): 0.29,
                     (False, False): 0.001
                     }
                    )
#        alarm.put([True, True], 0.95)
#        alarm.put([True, False], 0.94)
#        alarm.put([False, True], 0.29)
#        alarm.put([False, False], 0.001)
#        print alarm

        johncalls = CPT("J", ["A"], 
                        {
                        (True,): 0.9,
                        (False,): 0.05
                        }
                        )
#        johncalls.put([True], 0.90)
#        johncalls.put([False], 0.05)
#        print johncalls
#
        marycalls = CPT("M", ["A"], 
                        {
                        (True,) : 0.7,
                        (False,) : 0.01
                        }
                        )
#        marycalls.put([True], 0.7)
#        marycalls.put([False], 0.01)
#        print marycalls
        thing = CPT("T", [])
        thing.put([], 0.56)
        thing2 = CPT("T2", ["T"])
        bn = BNet()
        bn.add(burglary)
        bn.add(earthquake)
        bn.add(alarm)
        bn.add(johncalls)
        bn.add(marycalls)
#        bn.add(thing)
#        bn.add(thing2)

#        print "Relevant Nodes", bn.get_relevant(['J']).nodes
#        print "Children", bn.get_children('B')
        print bn.connection_check()
#        print bn.connection_check()
#        print bn.connection_check()
#        for i in bn.get_children('A'):
#            print "Children", i
#        print "Roots", bn.get_roots()
#        print "Get", alarm.get(True, [True, False])
#        print alarm.labels
#        earthquake.set_prior(.45)
#        print "E Get after prior set (T)", earthquake.get(True, [])
#        print "E Get after prior set (F)", earthquake.get(False, [])
        johncalls.instance = True
        marycalls.instance = True
#        earthquake.instance = False
#        alarm.instance = True
#        burglary.instance = True
#        print earthquake.get(True, [])

        test = bn.infer_naive(["B"])
        print test.log_likelihood()
        print test
        test = bn.infer_naive(["B", "E"])
        test.normalize()    
        print test.log_likelihood()
        print test
        print

        print "Setting earthquake=False"
        burglary.instance = None
        earthquake.instance = False
        test = bn.infer_naive(["B", "E"])
        print test.log_likelihood()
        test.normalize()
        print test
        print

        print "Setting burglary=True"
        earthquake.instance = None
        burglary.instance = True
        test = bn.infer_naive(["B", "E"])
        test.normalize()
        print test
        print
        
        print "old", bn.get_ancestors("B")
        print "old", bn.get_ancestors("J")
        print "old", bn.get_ancestors("M")
        print "old", bn.get_ancestors("A")
        x = CPT("Q", ["A", "M"])
        bn.add(x)
        print "old", bn.get_ancestors("Q")
        x = CPT("W", [])
        bn.add(x)
        x = CPT("R", ["W", "E", "B"])
        bn.add(x)
        print "old", bn.get_ancestors("R")


if __name__ == '__main__':
    test = SimpleExample()
#    import profile
#    profile.run('SimpleExample()')

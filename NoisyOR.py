'''
Created on Feb 13, 2012

@author: julianzaugg
'''

from CPT import CPT


class NoisyOR(CPT):
    """
    Noisy-OR implementation of conditional probability.
    It can be used as any other CPT, e.g. as a parent variable
    and as a latent variable in EM-training.
    """
    
    def get(self, status, key):
        """
        Retrieve the Noisy-OR filtered probability of a parent variable setting
        """
        pnot_true = 1.0
        for i in range(len(key)):
            if not key[i]:
                continue
            onekey = [False] * len(key)
            onekey[i] = True
            p = CPT.get(self, True, onekey)
            if p is None:
                return None
            pnot_true *= (1.0 - p)
        return 1.0 - pnot_true if status else pnot_true

    def maximize_instance(self):
        """
        Method for training the Noisy-OR CPT from the counts accumulated using countInstance.
        It implements the M-step in EM and resets the counts so beware.
        """
        for i in range(len(self.labels)):
            cptkey = [False] * len(self.labels)
            cptkey[i] = True
            p_true = self.count.get(cptkey + [True])
            p_false = self.count.get(cptkey + [False])
            if p_true != 0 or p_false != 0:
                self.put(cptkey, p_true / (p_true + p_false))
        self.count = None

    def put(self, key, prob):
        """
        Set the variable of this Noisy-OR CPT if the parent variables
        are set accordingly (one to True, rest to False)
        """
        if key.count(True) != 1:
            return
        CPT.put(self, key, prob)


if __name__ == '__main__':
    from Table_Utils import entry

    cpt1 = NoisyOR("fever", ["cold", "flu", "malaria"])
    cpt1.put([True, False, False], 0.4)
    cpt1.put([False, True, False], 0.8)
    cpt1.put([False, False, True], 0.9)

    for i in range(cpt1.maxrows):
        cptkey = entry(i, len(cpt1.labels))
        print cptkey, cpt1.get(True, cptkey), cpt1.get(False, cptkey)
    print cpt1
    print cpt1.get(True, [True, True, False])
    print cpt1.get(True, [True, False, True])


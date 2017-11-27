'''
Created on Dec 16, 2011

@author: julianzaugg
'''
#cython: profile=True

try:
    from cTable_Utils import entry
except ImportError, e:
    print e
    from Table_Utils import entry

import random
#import randomness as random
from JPT import JPT
from NumericBoolTable import NumericBoolTable

class CPT(NumericBoolTable):
    """
    Create a conditional probability table for a variable 
    with specified name. The variable is conditioned on 
    a set of boolean variables also specified.
    """
    def __init__(self, name, labels, table = None):
        NumericBoolTable.__init__(self, labels)
        self.name = name
        self.prior = None
        self.instance = None
        self.trainable = True
        if table:
            self.put_dict(table)
        #This is will be a JPT storing observations counts
        self.count = None

#    @profile
    def put(self, key, prob):
        """Set a entry of the CPT to the specified probability value."""
        assert 0 <= prob <= 1.0, "Probability value is invalid"
        if not key:
            self.set_prior(prob)
        else:
            NumericBoolTable.put(self, key, prob)      

    def put_dict(self, keys):
        """
        Set one or more entries to the specified probability values
        input(dict((bool_key) : value))
        """
        for key, prob in keys.iteritems():
            if key is None or key == ():
                self.set_prior(prob)
            else:
                NumericBoolTable.put(self, key, prob)

    def is_root(self):
        """Check if this CPT is a "root" CPT, i.e. has no parents."""
        if len(self.labels) == 0:
            return True
        return False

    def set_prior(self, value):
        """Set the prior value of a unconditioned CPT"""
        assert self.labels is not None, "Unable to set prior. CPT is conditioned"
        self.prior = value

    def get(self, status, key):
        """
        Get the conditional probability of the variable 
        (represented by this CPT) being set to a specified 
        status (true or false).
        A status value of 'None' will be considered False.
        """
        if not key:
            if self.prior is None:
                return None
            else:
                if status:
                    return self.prior
                else:
                    return 1.0 - self.prior
        p = NumericBoolTable.get(self, key)
        if p is None:
            return None

        return p if status else (1. - p)

    def randomize(self, seed, observations = None):
        """
        Put random entries into the CPT.
        Observations should be a list of observed values
        e.g    A      B     C      D     E
            [True, False, False, True, 0.2]
        """
        random.seed(seed)
        nrows = self.maxrows
        if nrows < 2:
            self.put([], random.random())
        else:
            for i in range(nrows):
                temp = entry(i, len(self.labels))
                self.put(temp, random.random())

    def count_instance(self, key, value, prob):
        """
        Count this observation. Note that for it (E-step in EM) to affect the
        CPT, maximize_instance must be called.
        """
        if self.count is None:
            self.count = JPT(self.labels + [self.name])
        if key is None:
            nkey = [value]
        else:
            nkey = key + [value]
        # FIXME: add here, but count elsewhere; what's the distinction?
        self.count.add(nkey, prob)

    def maximize_instance(self):
        """
        Take stock of all observations counted
        #i.e implement the M-step locally
        """
        self.count.normalize()
        for i in range(self.maxrows):
            cptkey = entry(i, len(self.labels))
            p_true = self.count.get(cptkey + [True])
            p_false = self.count.get(cptkey + [False])
            if p_true != 0 or p_false != 0:
                self.put(cptkey, p_true/(p_true + p_false))
        self.count = None

    def format_value(self, x):
        """Pretty-print of the value"""
        x = float(x)
        return "<%4.2f %4.2f>" % (x, 1-x)

    def __str__(self):
        if not self.labels:
            # Special case prior formatting
            string = "%10s" % self.name
            if self.prior is not None:
                string += "\t" + self.format_value(self.prior)
            return string
        else:
            return NumericBoolTable.__str__(self)


if __name__ == '__main__':
    cpt1 = CPT('v1', ['v2', 'v2', 'v3'])
    cpt1.put([True, False, False], 1.0)
    print cpt1
    jpt = JPT(["A", "B", "C", "D"])
    jpt.add([False, None, True, None], 0.2)
    jpt.add([True, True, True, None], 0.1)
    jpt.multiply([False, False, False, True], 0.1)
    print jpt
    jpt.normalize()
    print jpt
    

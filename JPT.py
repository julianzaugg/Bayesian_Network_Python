'''
Created on Dec 20, 2011

@author: julianzaugg
'''
#cython: profile=True

import math

from NumericBoolTable import NumericBoolTable


class JPT(NumericBoolTable):
    """
    A table representing a Joint Probability. The variables are all boolean.
    """

    def extend(self):
        """
        to be completed
        """

    def get(self, key):
        """
        Get the conditional probability of the variable 
        (represented by this JPT) being set to a specified 
        status (true or false).
        A status value of 'None' will be considered False.
        """
        y = NumericBoolTable.get(self, key)
        if y is None:
            return 0.0
        else:
            return y

    def normalize(self):
        """Normalizes the values in the JPT"""
        norm_constant = sum(self.map.values())
        # Check whether we're already normalized
        if norm_constant != 1.0:
            for entry in self.map:
                self.map[entry] /= norm_constant

    def log_likelihood(self):
        return math.log(sum(self.map.values()))


if __name__ == '__main__':
    jpt = JPT(["A", "B", "C", "D"])
    jpt.add([None, None, None, None], 0.2)
    jpt.add([True, True, True, None], 0.1)
    jpt.put([True, True, True, False], 0.1)
    jpt.multiply([False, False, False, True], 0.1)
    print jpt
    jpt.normalize();
    print jpt
    #jpt.extend("add", [False])
    #print jpt

'''
Created on Dec 13, 2011

@author: julianzaugg
'''
#cython: profile=True

try:
    from cBoolTable import BoolTable
except ImportError, e:
    print e
    from BoolTable import BoolTable
try:
    from cTable_Utils import indexer, indices
except ImportError, e:
    print e
    from Table_Utils import indexer, indices

class NumericBoolTable(BoolTable):
    """
    A table that stores numeric entries accessed via boolean key(s).
    """

    def get_sum(self, inputx):
        """
        Compute the sum of all entries matching the boolean key.
        Entries that match boolean key but do not have a value are
        assumed to be zero.
        """
        self.blength_check(inputx)
        total = 0.0
        for i in indices(inputx):
            y = self.map[i]
            if y is not None:
                total += y
        return total

    def get_prod(self, inputx):
        """
        Compute the product of all entries matching the boolean key.
        Note that entries that match the boolean key but do not have a
        value are assumed to be one (hence do not affect the result).
        """
        self.blength_check(inputx)
        prod = 1.0
        for i in indices(inputx):
            if i not in self.map:
                continue
            y = self.map[i]
            if y is not None:
                prod *= y
        return prod

    # FIX ME?: What happens when no entries in the current JPT?
    # Do we want it so if we try to add to a JPT with no labels
    # we 'recreate' the JPT to have entries valid to the inputx
    # and add the value to them? Otherwise the user is always
    # required to initialize the JPT with the labels they want...
    # An extend method would be helpful for this...
    def add(self, inputx, value):
        """
        Add a constant value to all entries matching the boolean key.
        A null Boolean key element represents "don't care".
        If a matching entry is null, a new entry is created 
        with specified value.
        """
        for i in indices(inputx):
            self.map[i] = self.map.get(i, 0.0) + value

    def multiply(self, inputx, value):
        """
        Add a constant value to the entry matching the boolean key.
        If the entry is null, then a new entry is created with 0.0 
        (previous value is considered zero).
        """
        self.blength_check(inputx)
        index = indexer(inputx)
        if index not in self.map:
            d = None
        else:
            d = self.map[index]
        if d is not None:
            nd = d * value
            self.map[index] = nd
            return nd
        else:
            self.map[index] = 0.0
            return value

    def format_value(self, value):
        """Pretty-print the value"""
        return "%9.4f" % value

if __name__ == '__main__':
    NTAB = NumericBoolTable(['A', 'B', 'C'])
    NTAB.put([True, True, False], 3.0)
    NTAB.put([False, True, True], -44.4)
    NTAB.put([True, False, False], 3.22)
    NTAB.add([True, False, False], 1.01)
    NTAB.add([None, None, False], 0.10)  
    print NTAB
    #print NTAB.get_sum([True, True, False])
    #print NTAB.get_prod([None, True, None])

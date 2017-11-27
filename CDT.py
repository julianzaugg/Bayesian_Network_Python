'''
Created on Jan 11, 2012

@author: julianzaugg
'''
#cython: profile=True

try:
    from cBoolTable import BoolTable
except ImportError, e:
    print e
    from BoolTable import BoolTable
try:
    from cTable_Utils import entry, indices
except ImportError, e:
    print e
    from Table_Utils import entry, indices


class CDT(BoolTable):
    '''
    This is a abstract class for Conditional Distribution Tables (CDTs).
    Sub-classes implementing it can not be "latent" nor "parent" nodes
    '''

    def __init__(self, name, labels):
        super(CDT, self).__init__(labels)
        self.name = name
        self.prior = None
        self.instance = None
        self.count = None
        self.trainable = True

    def is_root(self):
        """Check if this CPT is a "root" CPT, i.e. has no parents."""
        return len(self.labels) == 0

    def put(self, distr, key=None):
        """
        Set entry (or entries) of the CDT to
        the specified probability distribution
        """
        if key is None:
            self.prior = distr
        else:
            BoolTable.put(self, key, distr)

    def get(self, value, key):
        """
        Get the conditional probability of the variable
        (represented by this CDT) when set to a specified
        value.
        """
        if key is None:
            # FIXME: This prior handling is very different to the Java version
            if self.prior is not None:
                return self.prior
        d = BoolTable.get(self, key)
        if d is not None:
            p = d.get(value)
            return p
        return None

    def get_all(self, value):
        """
        Retrieve all the probabilities (densities if continuous) for a
        specified value for all entries in this table.
        Useful for normalization etc.
        """
        maxrows = self.maxrows()
        p = []
#        p =  [BoolTable.get(entry(i, len(self.labels))).get(value) for i in range(maxrows)]
        for i in range(maxrows):
            d = BoolTable.get(entry(i, len(self.labels)))
            p.append(d.get(value))
        return p

    def get_normalized(self, key, value):
        """
        Retrieve the (normalized) conditional
        probability of the specified value.
        """
        # FIXME: This is uncalled and untested.
        p = self.get_all(value)
        sumx = 0
        for i in p:
            sumx += i
        # FIXME: this looks wrong. Indices returns a list... should this be index?
        index = indices(key)
        return p[index] / sumx

    def count_instance(self, key, value, prob):
        """
        Count this observation. Note that for it
        (E-step in EM) to affect the CPT,
        maximizeInstance() must be called.
        """
        if self.count is None:
            self.count = BoolTable(self.labels)
        current = self.count.get(key)
        if current is None:
            current = {}
        if value in current:
            p = current.get(value)
        else:
            p = None
        if p is None:
            p = 0.0
        current[value] = prob + p
        self.count.put(key, current)

    def get_counts(self, key):
        """Get the value associated with the key from the counts JPT"""
        return self.count.get(key)

    def format_value(self, distrib):
        """pretty format value"""
        return "<%s>" % str(distrib)

    def __str__(self):
        if not self.labels:
            # Special case prior formatting
            string = "%10s" % self.name
            if self.prior is not None:
                string += "\t" + "<%s>" % str(self.prior)
            return string
        else:
            return BoolTable.__str__(self)

'''
Created on Dec 13, 2011

@author: julianzaugg
'''
#cython: profile=True

try:
    from cTable_Utils import entry, indexer
except ImportError, e:
    print e
    from Table_Utils import entry, indexer


class BoolTable(object):
    """
    Core container class for tables accessed by means of a Boolean "key".
    """
    def __init__(self, labels, nkey=None):
        """
        Create a table with a specified number of boolean attributes.
        """
        if not labels and nkey:
            labels = ["B%d" % (i + 1) for i in range(nkey)]
        if labels is None:
            labels = []
        self.labels = labels
        self.map = {}
        self.name = ''

    @property
    def maxrows(self):
        return 1 << len(self.labels)

    def blength_check(self, inputx):
        assert len(inputx) == len(self.labels), \
            "Length of boolean key is invalid; expected %d got %d" \
            % (len(self.labels), len(inputx))

    def get_key_indices(self, label_list):
        """
        Get the indices in the key for this table that correspond to the
        specified labels (same order as the labels).
        """
        keyindexer = []
#        print label_list, self.labels
#        print label_list in self.labels
        for i in [label_list]:
            if i in self.labels:
                return self.labels.index(i)
            else:
                assert False, "Failed to match a label to the table %s" % i
            keyindexer.append(i)
        return keyindexer

    def get(self, inputx):
        """Get the value that is associated with the boolean key."""
        try:
            return self.map[indexer(inputx)]
        except KeyError:
            return None

    def put(self, inputx, value):
        """Put a value in entry associated with boolean key."""
#        self.blength_check(inputx)
        index = indexer(inputx)
        self.map[index] = value

    def put_dict(self, keys):
        """
        Takes a dictionary of key : values, setting boolean keys
        in table to values.
        """
        for key, prob in keys.iteritems():
            self.put(key, prob)

    # **************************************************
    # FIX ME: DELETE?
    def is_true(self, ncol, index):
        """
        Test if the index corresponds to a key with "true"
        in the specified column.
        """
        nround = self.maxrows + 1
        n = index % nround / 2
        return n < nround / 2

    def joinerer(self, col1, col2, indexer1, indexer2):
        """Test if the two keys agree (join) at two indices"""
        return self.is_true(col1, indexer1) == self.is_true(col2, indexer2)
    # **************************************************

    def format_value(self, value):
        """placeholder"""
        return value

    def __str__(self):
        header_row = "\t".join(self.labels)
        header_row += "%10s" % self.name
        string = [header_row]
        for i in sorted(self.map.keys()):
            bkey = entry(i, len(self.labels))
            row_str = "\t".join(["T" if b else "F" for b in bkey])
            row_str += "\t %s" % self.format_value(self.map[i])
            string.append(row_str)
        return "\n".join(string)

if __name__ == '__main__':
    BTAB = BoolTable([], 3)
    BTAB.put([True, True, False], 3.0)
    BTAB.put([False, True, True], -44.4)
    BTAB.put([True, False, False], 3.22)
    print "\n"
    print BTAB
    print "\n"
    print BTAB.get([True, True, False])
    print BTAB.get([False, None, None])
    print BTAB.get([True, False, True])
    print BTAB.is_true(4, 16)

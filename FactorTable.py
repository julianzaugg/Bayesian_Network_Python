'''
Created on Dec 21, 2011

@author: julianzaugg
'''
import math
from NumericBoolTable import NumericBoolTable
from CPT import CPT
import JPT

class FactorTable(NumericBoolTable):
    '''
    WORK IN PROGRESS
    The main data structure for bucket/variable elimination that 
    performs exact inference in Bayesian networks.
    '''

    def __init__(self, cpt):
        '''
        Create a standard factor table for the CPT.
        The procedure checks if the CPT is instantiated,
        i.e. that the variable has a specified value.
        If so, it does not include the variable in the list of
        conditional variables.
        '''
        temp = self.extract_variable_names(cpt)
        NumericBoolTable.__init__(self, len(temp), temp)
        self.name = cpt.name
        self.no_param_value = 0.0
        nrows = cpt.get_step(len(cpt.labels))
        if cpt.instance is None:
            for e in range(nrows):
                ckey= cpt.entry(e)
                fkey = []
                fkey.append(True)
                for j in ckey:
                    fkey.append(j)
                p = cpt.get(ckey, fkey[0])
                if p:
                    self.put(fkey, p)
                    fkey[0] = False
                    self.put(fkey, 1 - p)
        else:
            if len(cpt.labels) == 0:
                p = cpt.get(cpt.instance)
                if p:
                    self.put(fkey, p)
            else:
                for i in range(nrows):
                    fkey = self.entry(i, len(cpt.labels))
                    p = cpt.get(cpt.instance, fkey)
                    if p is not None:
                        self.put(fkey, p)

    def extract_variable_names(self, cpt):
        """
        placeholder
        """
        parents = cpt.labels
        if cpt.instance is not None:
            return parents
        else:
            arr = []
            arr.append(cpt.name)
            arr = [i for i in parents]
            return arr

    def remove_variable_name(self, orig, removeme):
        """
        placeholder
        """
        cnt = 0
        i = 0
        arr = [x for x in range(len(orig - 1))]
        while i < len(orig) and cnt < len(arr):
            if orig[i] != removeme:
                arr[cnt] = orig[i]
                cnt += 1
                i += 1
        return arr

    #this is horribly wrong
    def union_variable_names(self, list1, list2):
        """
        placeholder
        probably can be rewritten, we just want to
        make a list of variable names without duplicates
        however this can be done once we start actually using the method
        """
        cnt = 0
        if not list1 or not list2:
            list1 = list2
        overlap = []
        for i in list1:
            for j in list2:
                if i == j:
                    overlap.append(True)
                    cnt += 1
                    break
        ret = []
        for i in list1:
            ret.append(i)
        cnt = 0
        for i in list2:
            if i not in overlap:
                ret.append(i)

    def select(self, var, value):
        """
        placeholder
        """
        varsx = self.labels
        for v in varsx:
            if v == var:
                return FactorTable(self, var, value)

    def get(self, key):
        """
        placeholder
        """
        if not key:
            return self.no_param_value
        p = NumericBoolTable.get(self, key)
        if not p:
            return p
        else:
            return 0.0

    def put(self, key, value):
        """
        placeholder
        """
        if not key:
            self.no_param_value = value
        else:
            NumericBoolTable.put(self, key, value)

    def get_log_likelihood(self):
        """
        placeholder
        """
        sumx = 0
        for p in self.map.values():
            if not p:
                sumx += p
        return math.log(sum)
    
    def product(self, factor1, factor2):
        """
        return the product of two factor tables
        ERRORS?! specifically when to refer to self!
        """
        fnames = self.union_variable_names(factor1.labels, factor2.labels)
        NumericBoolTable.__init__(self, len(fnames), fnames)
        self.name = "[" + factor1.name + "*" + factor2.name + "]"
        maxrows = self.get_step(len(self.labels))
        for i in range(maxrows):
            mykey = self.entry(i, maxrows)
            f1key = []
            f2key = []
            for j in mykey:
                f1key.append(j)
            keyindex = self.get_key_indices(factor2.labels)
            #fix
            for j in range(len(factor2.labels)):
                f2key.append(mykey[keyindex[j]])
            p1 = factor1.get(f1key)
            p2 = factor2.get(f2key)
            if not p1 and not p2:
                self.put(mykey, p1*p2)
            else:
                self.put(mykey, 0.0)
        return FactorTable()
    
    def get_jpt(self, varnames):
        jpt = JPT(len(varnames), varnames)
        keyindices = self.get_key_indices(varnames)
        jkey = []
        maxrows = jpt.get_step(len(varnames))
        for i in range(maxrows):
            fkey = self.entry(i, len(varnames))
            value = self.get(fkey)
            if value is not None:
                for v in fkey:
                    jkey.append(v)
                jpt.put(jkey, value)
        jpt.normalize()
        return jpt

    def __str__(self):
    
        string = ""
        for s in range(len(self.labels)):
            string += self.labels[s]
            if s < len(self.labels) -1:
                string += ","
            else:
                string += ":"
        temp =  "FT^" + self.name + "(" + string + ")"
        return temp + "\n" + NumericBoolTable.__str__(self)
    



if __name__ == '__main__':
    cpt1 = CPT('A', ['B', 'C', 'D'])
    cpt1.put([True, True, False], .45)
    print cpt1
    ft = FactorTable(cpt1)
    print 'FTable name :', ft.name
    print ft
    
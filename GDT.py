'''
Created on Jan 11, 2012

@author: julianzaugg
testing again
'''
#cython: profile=True

try:
    from cTable_Utils import entry
except ImportError, e:
    print e
    from Table_Utils import entry

from CDT import CDT
from Gaussian import Gaussian

class GDT(CDT):

    def __init__(self, name, labels,):
        """Constructor"""
        CDT.__init__(self, name, labels)
        self.tie_variances = False
        self.USE_MAX_VARIANCE = True

    def randomize(self, seed, observations):
        """
        Set an entry of the GDT to a Gaussian distribution based on
        observations.
        """
        minx = 0
        maxx = 0
        sumx = 0
        var = 0
        for i in range(len(observations)):
            y = observations[i]
            sumx += y
            if i == 0:
                maxx = minx = y
            else:
                if y > maxx:
                    maxx = y
                elif y < minx:
                    minx = y
        mean = sumx/len(observations)
        for i in observations:
            y = i
            var += (mean - y) * (mean - y)
        var /= len(observations)
        nrows = self.maxrows
        if nrows < 2:
            self.put(Gaussian(mean, var))
        else:
            rangex = maxx - minx
            stepsize = rangex/nrows
            for i in range(nrows):
                self.put(Gaussian((maxx - stepsize * i) - stepsize / 2, var),
                         entry(i, len(self.labels)))

    def maximize_instance(self):
        maxrows = self.maxrows
        #The largest variance of any class
        maxvar = 0
        #save the means
        means = [0] * maxrows
        #save the variances
        varsx = [0] * maxrows
        #the mean of all values
        middlemean = 0
        #the variance of all values
        middlevar = 0
        #the sum of count for all parent configs
        middletot = 0
        #go through each possible setting of the parent nodes
        for i in range(maxrows):
            #The values of the parent nodes
            key = entry(i, len(self.labels))
            #The frequencies or counts of each "value" GIVEN parents,
            #e.g. for a single parent config there are 4x "0.5 if the parent
            #is "true" (where "4" is the count)
            count = self.get_counts(key)
            #we keep track of the sum of observed values for a specific parent
            #config weighted by count, e.g 4 x 0.5 + 3 x 1.3 + ...
            sumx = 0
            #We keep track of the total of counts for a specific parent config
            #so we can compute the mean of values, e.g there are 23 counted
            #for parent is "True"
            total = 0
            #just to be safe...we ignore configs that have no counts
            if count is not None:
                #the observations, i.e observed values or scores
                y = [0] * len(count)
                #how often do we see this score GIVEN the parents
                #(an absolute count)
                p = [0] * len(y)
                j = 0
                #Look at each value entry
                for k, v in count.iteritems():
                    #actual value (or score)
                    y[j] = k
                    #p(class=key) i.e the height of the density for this
                    #parent config
                    p[j] = v
                    #update the numerator of the mean calc
                    sumx += (y[j] * p[j])
                    #update the denominator of the mean calc
                    total += p[j]
                    j += 1
                means[i] = (sumx/total)
                diff = 0
                jj = 0
                for jj in range(len(y)):
                    diff += (means[i] - y[jj])*(means[i]-y[jj])*p[jj]
                varsx[i] = diff/total
                if varsx[i] < 0.01:
                    varsx[i] = 0.01
                if varsx[i] > maxvar:
                    maxvar = varsx[i]
                self.put(Gaussian(means[i], varsx[i]), key)
                middletot += total
                middlemean += sumx
        middlemean /= middletot
        #re-compute variances if they need to be tied
        #there are different ways of dealing with this
        if self.tie_variances:
            # (1) Simply use the max of the existing variances
            if self.USE_MAX_VARIANCE:
                for i in range(maxrows):
                    key = entry(i, len(self.labels))
                    self.put(Gaussian(means[i], maxvar), key)
            else:
                # (2) compute the variance of all the values
                for i in range(maxrows):
                    key = entry(i, len(self.labels))
                    count = self.get_counts(key)
                    if count is not None:
                        #The observations, i.e observed values of scores
                        y = [0] * len(count)
                        #How often do we see this score GIVEN the parents
                        #(an absolute count)
                        p = [0] * len(y)
                        j = 0
                        for k, v in count.iteritems():
                            #actual score
                            y[j] = k
                            #p(class = key) i.e the height of the density for
                            #this parent config
                            p[j] = v
                            j += 1
                        diff = 0
                        jj = 0
                        while jj < len(y):
                            diff += ((middlemean - y[jj]) *
                                     (middlemean - y[jj])*p[jj])
                            jj += 1
                        var = diff/middletot
                        if var < 0.01:
                            var = 0.01
                        self.put(Gaussian(means[i], var), key)

'''
Created on Jan 11, 2012

@author: julianzaugg
'''
#cython: profile=True

import math
import random
#import randomness as random

class Gaussian(object):
    """The multivariate Gaussian density function"""


    def __init__(self, mean, variance):
        """Constructor"""
        self.mu = mean
        self.sigma = 0
        self.sigmasquared = 0
        self.normconst = 0
        self.lognormconst = 0
        self.ROOT_2PI = math.sqrt(2 * math.pi)
        self.LOG_ROOT_2PI = 0.5 * (math.log(2) + math.log(math.pi))
        self.set_variance(variance)

    def get(self, inputx):
        """get the density value for the input"""
        return self.get_density(inputx)

    def get_density(self, x):
        """
        Returns a value sample from this Gaussian distribution. This method
        should only be called if the mean and variance were set in the
        constructor (internal calls are 'ok' if the private method
        init_params is called first.
        """
        assert isinstance(x, float), "Expected float, got %s" % repr(x)
        return math.exp(-math.pow((x - self.mu), 2)/
                        (2 * self.sigmasquared)) / self.normconst

    def get_log_density(self, x):
        """
        Returns the natural log of the density of this Gaussian distribution.
        This method should only be called if the mean and variance were set
        in the constructor (internal calls are 'ok' if the private method
        init_params is called first).
        """
        return (-math.pow((x - self.mu), 2) / \
            (2 * self.sigmasquared)) - self.lognormconst

    def sample_val(self):
        """
        Returns a value sample from this Gaussian distribution. This method
        should only be called if the mean and variance were set in the
        constructor (internal calls are 'ok' if the private method
        init_params is called first.
        """
        U = random.random()
        V = random.random()
        return (self.mu + (self.sigma * math.sin(2 * math.pi * V) * 
                           math.sqrt((-2 * math.log(U)))))

    def set_variance(self, variance):
        """Set the variance"""
        self.sigmasquared = variance
        assert not self.sigmasquared <= 0, "Variance of UnivarGaussian\
                                            distribution must be positive,\
                                            not " + self.sigmasquared
        self.sigma = math.sqrt(self.sigmasquared)
        self.normconst = self.sigma * self.ROOT_2PI
        self.lognormconst = (0.5 * math.log(self.sigmasquared)) + \
                            self.LOG_ROOT_2PI

    def randomize(self, seed):
        """Randomize the mean and variance"""
        random.seed(seed)
        self.mean = random.gauss(0., 1.)
        self.set_variance(random.random())

    def __str__(self):
        """Pretty format the mean and variance"""
        return "%4.2f;%4.2f" % (self.mu, self.sigmasquared)


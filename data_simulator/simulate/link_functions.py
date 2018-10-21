"""
Link Functions
"""
from numpy import exp, log


def inv_logit(x):
    return 1./(1. + exp(-1*(x)))


def logit(prob):
    return log((prob) / (1 - prob))


def identity(x):
    return x

"""
Models to simulate data from
"""
from enum import Enum
from numpy import random, vectorize
from numpy.linalg import cholesky
from data_simulator.simulate.link_functions import inv_logit, identity
from data_simulator.simulate.matrix_functions import set_matrices


class Types(Enum):

    @classmethod
    def values_list(cls):
        return [type_.value for type_ in list(cls)]

    @classmethod
    def names_list(cls):
        return [type_.name.lower() for type_ in list(cls)]

    @classmethod
    def tuple_pair(cls):
        return list(zip(map(lambda x: str(x),
                            cls.values_list()),
                        map(lambda x: x.replace("_", " "),
                            cls.names_list())))


class ModelNames(Types):
    LINEAR_REGRESSION = 1
    LOGISTIC_REGRESSION = 2


vint = vectorize(lambda x: int(x))


def simulate_from_mvn_covariance_structure(nobs, nvars,
                                           mean_vector,
                                           covariance_matrix):
    """
    Simulates data given a covariance structure.
    Assumes a multivariate normal distribution.
    :param mean_vector: A numpy array
    :param covariance_matrix:
    :param nparams:
    :param nobs:
    """
    simulated_data = random.normal(
        0, 1, nobs*nvars).reshape(nobs, nvars).dot(
        cholesky(covariance_matrix).T) + mean_vector
    return simulated_data


"""
Models
"""


def linear_regression_simulation_ys(nobs, xs, param_matrix, ymeans=None,
                                    yvars=None):
    """
    y = x*B + e
    e ~ N(0, sigma^2)
    """
    if ymeans is None:
        ymeans = [0]
    if yvars is None:
        yvars = [1]
    vals = identity(xs.dot(param_matrix))
    e_mean, e_varcov = set_matrices(1, ymeans, yvars)
    es = simulate_from_mvn_covariance_structure(
        nobs, 1, e_mean, e_varcov)
    ys = vals + es
    return ys


def linear_regression_simulation_cond_ys(nobs, xs, param_matrix,
                                         ymeans, yvars):
    """
    E(y | x*B) = x*B
    y ~ N(mu, sigma^2)
    """
    vals = identity(xs.dot(param_matrix))
    mean_y, var_y = set_matrices(1, ymeans, yvars)
    cond_ys = simulate_from_mvn_covariance_structure(
        nobs, 1, mean_y, var_y)
    ys = vals + cond_ys
    return ys


def logistic_regression_simulation_binomial_ys(nobs, xs, param_matrix,
                                               ymeans=None, yvars=None):
    """
    Method 1: simulate y values from binomial distribution using
    logit link
    This approach assumes the intercept was used
    """
    probs = inv_logit(xs.dot(param_matrix))
    ys = random.binomial(1, probs)
    return ys


def logistic_regression_simulation_uniform_ys(nobs, xs, param_matrix,
                                              ymeans=None, yvars=None):
    """
    Method 2: simulate random uniform values from a
    U ~ (0, 1) distribution and if each u_i value is
    less than prob_i, then y_i=1, else y_i=0
    This approach assumes the intercept was used
    """
    probs = inv_logit(xs.dot(param_matrix))
    us = random.uniform(0, 1, nobs).reshape(nobs, 1)
    ys = vint(us <= probs)
    return ys


def logistic_regression_simulation_ystars(nobs, xs, param_matrix,
                                          ymeans, yvars=None):
    """
    Method 3: underlying latent variable approach.
    Can specify a conditional mean for y here
    beta should NOT contain an intercept
    Y_i* = beta*x + e where e ~ logistic(b0, 1)
    """
    y_stars = xs.dot(param_matrix) + random.logistic(
        ymeans, 1, nobs).reshape(nobs, 1)
    ys = vint(y_stars > 0.)
    return ys

from numpy import array, zeros, tril_indices, diag, ones, append


def add_constant(numpy_array):
    numpy_array_with_constant = append(ones(numpy_array.shape[0]).reshape(
        numpy_array.shape[0], 1), numpy_array, 1)
    return numpy_array_with_constant


def set_matrices(n, means=None, varcovs=None):
    """
    varcovs is a list with elements in the order:
        V1 V2 V3 V4
     V1 1
     V2 2  3
     V3 4  5  6
     V4 7  8  9  10
    if the above is a covariance matrix of 4 variables
    """
    if means is not None:
        mean_vector = array(means).reshape(1, n)
    if varcovs is not None:
        varcov_matrix = zeros(n * n).reshape(n, n)
        varcov_matrix[tril_indices(n)] = varcovs
        varcov_matrix = varcov_matrix.T + (
            varcov_matrix - diag(diag(varcov_matrix)))
    return (mean_vector, varcov_matrix)


def set_parameter_matrices(params):
    nparams = len(params)
    return array(params).reshape(nparams, 1)

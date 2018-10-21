import json
import sys
from numpy import hstack
from pandas import DataFrame
from data_simulator.simulate.matrix_functions import (
    set_matrices, set_parameter_matrices,
    add_constant)
from data_simulator.simulate.simulation_models import (
    ModelNames, simulate_from_mvn_covariance_structure,
    linear_regression_simulation_cond_ys,
    logistic_regression_simulation_binomial_ys)
from data_simulator.model_utils.model_structure import (
    ModelStructure)

"""
Data Simulation Entry Point
"""


def get_json(filename):
    try:
        json_file = open(filename)
    except IOError:
        print("Wrong file or file path")
        sys.exit(1)
    json_string = json_file.read()
    try:
        return json.loads(json_string)
    except ValueError:
        print("Error loading json")
        sys.exit(1)


def write_data(xs, ys, datafile):
    all_vals = hstack((xs, ys))
    d = DataFrame(all_vals)
    d.to_csv(datafile, index=False, header=None)


def plot_data(xs, ys):
    pass


def set_model_struc_obj(model_name, json):
    model_struc = ModelStructure(model_name, json)
    model_struc.deserialize_json()
    return model_struc


def command_line_entry(json_filename, model_name,
                       nobs, output_filename):
    json = get_json(json_filename)
    model_struc = set_model_struc_obj(model_name, json)
    sim_xs, sim_ys = run(model_name, nobs, model_struc.nx,
                         model_struc.get_x_variable_mean_values(),
                         model_struc.x_varcovs, model_struc.ny,
                         model_struc.params,
                         model_struc.get_y_variable_mean_values(),
                         model_struc.y_varcovs)
    write_data(sim_xs, sim_ys, output_filename)
    return model_struc


def run(model_name, nobs, nx, x_means, x_varcovs,
        ny, params, y_means=None, y_varcovs=None):
    x_mean_vector, x_varcov_matrix = set_matrices(nx, x_means, x_varcovs)
    y_mean_vector, y_varcov_matrix = set_matrices(ny, y_means, y_varcovs)
    param_matrix = set_parameter_matrices(params)
    sim_xs = simulate_from_mvn_covariance_structure(
        nobs, nx, x_mean_vector, x_varcov_matrix)
    if model_name.lower(
    ) == ModelNames.LINEAR_REGRESSION.name.lower():
        sim_ys = linear_regression_simulation_cond_ys(
            nobs, sim_xs, param_matrix,
            y_mean_vector, y_varcov_matrix)
    elif model_name.lower(
    ) == ModelNames.LOGISTIC_REGRESSION.name.lower():
        sim_ys = logistic_regression_simulation_binomial_ys(
            nobs, add_constant(sim_xs), param_matrix)
    return sim_xs, sim_ys

"""
runmain takes and validates command line arguments and
runs simulation
"""
from argparse import ArgumentParser
import sys
from data_simulator.simulate.simulation_models import ModelNames
from data_simulator.simulate.simulate_data import command_line_entry


def main(args=None):
    """
    Main method that parses command line arguments and calls run method
    """
    if args is None:
        args = sys.argv[1:]
    else:
        print(args)
    parser = ArgumentParser(
        description='''Simulate data according to a statistical
        model''')
    parser.add_argument(
        '--json-file', type=str, required=True,
        dest='json_file', help='''json file containing model structure
        and parameter values''')
    parser.add_argument(
        '--model-name', type=str, required=True,
        dest='model_name',
        choices=[m.name.lower() for m in ModelNames],
        help="Can be one of: {}".format(
            ", ".join([m.name.lower() for m in ModelNames])))
    parser.add_argument(
        '--nobs', type=int, required=True,
        dest='nobs',
        help='Number of observations to simulate')
    parser.add_argument(
        '--output-file', type=str, required=True,
        dest='output_file',
        help="Name of file to output data to")
    options = parser.parse_args(args)
    output = command_line_entry(
        options.json_file, options.model_name,
        options.nobs, options.output_file)
    return output

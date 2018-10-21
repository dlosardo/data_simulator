#!/usr/bin/env python3

from setuptools import setup
from os import path


def get_requirements():
    """Reads the installation requirements from requirements.pip"""
    with open("requirements.pip") as f:
        lines = f.read().split("\n")
        requirements = list(filter(lambda l: not l.startswith('#'), lines))
        return requirements


here = path.abspath(path.dirname(__file__))

setup(name='data_simulator',
      description='Simulates data according to a statistical model',
      long_description='',
      author='Diane Losardo',
      url='todo',
      download_url='todo',
      author_email='dlosardo@gmail.com',
      version='0.1',
      install_requires=get_requirements(),
      packages=['data_simulator', 'data_simulator/simulate',
                'data_simulator/model_utils'
                ],
      package_dir={'data-simulator': ''},
      scripts=['bin/run_simulation.py']
      )

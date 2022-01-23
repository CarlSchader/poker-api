#!/bin/bash

cythonize -i *.py
cython simulator.py --embed

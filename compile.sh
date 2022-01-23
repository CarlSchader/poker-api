#!/bin/bash

MODULES=("card" "compare" "generate" "ranks" "validation")

for i in "${MODULES[@]}"
do
    cythonize -i "${i}.py"
done

LIBS=()

for i in *.so
do
    LIBS+=$(basename $i .so)
done

cython simulator.py --embed

# gcc simulator.c

# rm -rf *.c
# rm -rf *.so
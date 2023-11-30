#!/bin/bash

function plot {
    python3 py/plot.py $1
    
}

export -f plot
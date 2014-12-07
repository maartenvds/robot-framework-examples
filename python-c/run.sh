#!/bin/bash

PWD=`pwd`
export PYTHONPATH="$PWD/lib/"

pybot --outputdir output $@

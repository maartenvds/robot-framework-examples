#! /usr/bin/env python

import os
import sys
from tempfile import TemporaryFile
from subprocess import Popen, call, STDOUT

import Selenium2Library

WEBSERVER = "target/server.py"
OUTDIR = "output"

def start_web_server():
    Popen(['python', WEBSERVER, 'start'], stdout=TemporaryFile(), stderr=STDOUT)

def stop_web_server():
    call(['python', WEBSERVER, 'stop'], stdout=TemporaryFile(), stderr=STDOUT)

def run_tests(args):
    start_web_server()
    call(['mkdir', '-p', OUTDIR])
    call(['pybot', '--outputdir', OUTDIR] + args, shell=(os.sep == '\\'))
    stop_web_server()

if __name__ == '__main__':

    run_tests(sys.argv[1:])

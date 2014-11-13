#! /usr/bin/env python

import os
import sys
from tempfile import TemporaryFile
from subprocess import Popen, call, STDOUT

import Selenium2Library

ROOT = os.path.dirname(os.path.abspath(__file__))
DEMOAPP = os.path.join(ROOT, 'target', 'server.py')

def run_tests(args):
    start_demo_application()
    call(['pybot'] + args, shell=(os.sep == '\\'))
    stop_demo_application()

def start_demo_application():
    Popen(['python', DEMOAPP, 'start'], stdout=TemporaryFile(), stderr=STDOUT)

def stop_demo_application():
    call(['python', DEMOAPP, 'stop'], stdout=TemporaryFile(), stderr=STDOUT)

if __name__ == '__main__':

    run_tests(sys.argv[1:])

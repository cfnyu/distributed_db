# -*- coding: utf-8 -*-
""" CLI Argument Parser

    Utility class to help parse CLI arguments for testing
"""
import sys
from logger import init_logger, log

def validate_args():
    """ This code is intended to test is class from the CLI """
    if len(sys.argv) < 2 or sys.argv[1] == '-v':
        print "To parse a file use the following command: parser.py <file_name> [-v]"
        return False

    log("Starting parse function " + str(sys.argv))

    if len(sys.argv) > 2 and sys.argv[2] == '-v':
        print "Verbose set to true"
        init_logger(True)

    return True

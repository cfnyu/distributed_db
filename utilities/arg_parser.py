# -*- coding: utf-8 -*-
""" CLI Argument Parser

    Utility class to help parse CLI arguments for testing
"""
import sys
from logger import init_logger, log

def validate_args(required_arg_num=0, err_msg=""):
    """ This code is intended to test is class from the CLI """
    if len(sys.argv) < required_arg_num + 1:
        print err_msg
        return False

    if sys.argv[len(sys.argv) - 1] == '-v' or sys.argv[1] == "-v":
        print "Verbose set to true"
        init_logger(True)

    return True

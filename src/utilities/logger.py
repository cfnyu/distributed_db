# -*- coding: utf-8 -*-
""" Logger

    This file holds all utility methods used for logging parts of the application
    To assit with debugging
"""

VERBOSE = False

def log(value):
    """Add a string that will be printed to the stdout if the VERBOSE flag is true"""
    global VERBOSE

    if VERBOSE:
        if isinstance(value, list):
            print "######### List Results #########"

            for i, val in enumerate(value):
                print str(i+1) + ":", str(val)

        else:
            print value
    else:
        return 0       

def init_logger(value):
    """ Set the VERBOSE flag """
    global VERBOSE

    VERBOSE = value

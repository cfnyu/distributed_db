# -*- coding: utf-8 -*-
""" Logger

    This file holds all utility methods used for logging parts of the application
    To assist with debugging
"""

class Logger:
    """ System logger """

    def __init__(self):
        self.verbose = False

    def log(self, value):
        """Add a string that will be printed to the stdout if the VERBOSE flag is true"""

        if self.verbose:
            if isinstance(value, list):
                print "######### List Results #########"

                for i, val in enumerate(value):
                    print str(i+1) + ":", str(val)

            else:
                print value
        else:
            return 0

    def show_stdout(self):
        """ Set the Verbose flag to True"""

        self.verbose = True

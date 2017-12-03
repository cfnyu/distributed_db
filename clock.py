# -*- coding: utf-8 -*-
""" Clock

This model represents the database clock.

"""

from utilities.logger import log
from utilities.arg_parser import validate_args

class Clock:
    """ Maintain a numerical value that represents the 'System Time' """

    def __init__(self):
        """ Clock Constructor """

        self.time = 0

    def __repr__(self):
        """ The current state of the Clock object """

        return "<Time: %i>" % self.time

    def tick(self):
        """ Increase the time by one """
        
        self.time += 1

def main():
    """ This code is intended to test the Clock class from the CLI """

    err = "To check the clock file, use the following command: python clock.py [-v]"

    if validate_args(err_msg=err):
        clock = Clock()
        clock.tick()
        log(str(clock))
        clock.tick()
        log(str(clock))

if __name__ == "__main__":
    main()

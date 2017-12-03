# -*- coding: utf-8 -*-
""" Clock

This model represents the database clock.

"""

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

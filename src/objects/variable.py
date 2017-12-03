# -*- coding: utf-8 -*-
""" Variable

This module represents a variable as specified in the Homework

"""

class Variable:
    """ Maintains all things related to a variable """

    def __init__(self, var_id):
        self.index = var_id
        self.replicated = (var_id / 2 == 0)
        self.readable = True
        # self.log = {}
        # self.log[time] = 10 * var_id # Starting value for this Variable

    def __repr__(self):
        return "x%i" % self.index

    # def current_value(self):
    #     """ Returns the last known committed value for this variable """
    #     return self.log[-1]

    # def get_value_by_time(self, time):
    #     """ Returns the last known committed value for this variable """
    #     return self.log[-1]

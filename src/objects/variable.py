# -*- coding: utf-8 -*-
""" Variable

This module represents a variable as specified in the Homework

"""

class Variable:
    """ Maintains all things related to a variable """

    def __init__(self, time, var_id):
        self.index = var_id
        self.identifier = "x%i" % self.index
        self.replicated = (var_id / 2 == 0)
        self.readable = True
        self.value = 10 * var_id
        self.written_values = {}
        self.update_value(time, self.value)

    def __repr__(self):
        return "{ %s: %s }" % (self.identifier, self.value)

    def update_value(self, time, new_value):
        """ Update the current variable value """

        self.value = new_value
        self.written_values[time] = new_value

    def get_last_committed_value(self):
        """ Returns the last committed value from the log """

        return self.written_values[sorted(self.written_values.keys(), \
                                          reverse=True)[0]]

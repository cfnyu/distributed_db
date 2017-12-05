# -*- coding: utf-8 -*-
""" Variable

This module represents a variable as specified in the Homework

"""

class Variable:
    """ Maintains all things related to a variable """

    def __init__(self, var_id):
        self.index = var_id
        self.identifier = "x%i" % self.index
        self.replicated = (var_id / 2 == 0)
        self.readable = True
        self.value = 10 * var_id
        self.last_committed_value = self.value

    def __repr__(self):
        return "{ %s: %s }" % (self.identifier, self.value)

# -*- coding: utf-8 -*-
""" Lock Manager

This module represents the Lock Manager used by a Data Manager
To manage the locks on a single site

"""

class LockManager:
    """ Maintains all Locks for a particular site """

    def __init__(self):
        self.entries = {}
        #self.entries[time] = 10 * var_id # Starting value for this Variable

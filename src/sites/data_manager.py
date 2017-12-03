# -*- coding: utf-8 -*-
""" Data Manager

This module represents the Data Manager, which manages all
Site specific data

"""

class DataManager:
    """ Maintains all data for a particular site """

    def __init__(self):
        self.entries = {}
        #self.entries[time] = 10 * var_id # Starting value for this Variable

    def log(self, variable, time, value):
        """ Log all variable changes. """

        if not variable in self.entries:
            self.entries[variable] = {}

        # The assumption here is 'Time' is a unique number
        self.entries[variable][time] = value

    def get_variable_value(self, variable):
        """ Returns the last known committed value for this variable """

        if variable in self.entries:
            # Sort all values by key for a particular variable value in decending order
            # And return the first value, which should represent the last commit value
            # For this variable
            time_idx = 0
            value_idx = 1
            return sorted(self.entries[variable].items(),
                          key=lambda kv: kv[time_idx], reverse=True)[0][value_idx]

    def get_variable_at_time(self, variable, time):
        """ Returns the last known committed value for this variable """

        if variable in self.entries:
            return self.entries[variable][time]

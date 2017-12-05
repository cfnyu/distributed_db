# -*- coding: utf-8 -*-
""" Data Manager

This module represents the Data Manager, which manages all
Site specific data

"""

class DataManager:
    """ Maintains all data for a particular site """

    def __init__(self):
        self.entries = {}
        self.variables = {}
        self.up_time = 0

    def log(self, variable, time):
        """ Log all variable changes. """

        if variable.identifier not in self.entries:
            self.entries[variable.identifier] = {}

        # The assumption here is 'Time' is a unique number
        self.entries[variable.identifier][time] = variable

    def add_variable(self, time, variable):
        """ Method to add a new variable that will be managed by this DM """

        self.variables[variable.identifier] = variable

        # Starting initial variable value
        self.log(variable, time)

    def get_variable_value(self, identifier):
        """ Returns the last known committed value for this variable """

        return self.variables[identifier].value

        # if variable in self.entries:
        #     # Sort all values by key for a particular variable value in decending order
        #     # And return the first value, which should represent the last commit value
        #     # For this variable
        #     time_idx = 0
        #     value_idx = 1
        #     return sorted(self.entries[variable].items(),
        #                   key=lambda kv: kv[time_idx], reverse=True)[0][value_idx]

    def get_variable_at_time(self, variable, time):
        """ Returns the last known committed value for this variable """

        if variable in self.entries:
            return self.entries[variable][time].value

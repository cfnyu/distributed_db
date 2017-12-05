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
        self.locks = {}

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
            if not time in self.entries[variable]:
                return self.get_variable_at_time(variable, time-1)
            else:
                return self.entries[variable][time].value

    def get_variable_object(self, variable_ident):
        """ Returns the variable object for the variable_ident """
        return variables[variable.variable_ident]

    def obtainWriteLock(self, instruction, transaction):
        lock_type = LockType.WRITE

        variable_ident = instruction.variable_identifier
        variable = get_variable_object(variable_ident)

        if variable_ident not in locks: 
            lock = Lock(lock_type, transaction, variable)
            locks[variable_ident] = [lock]
            return true
        else:
            lock_list = locks[variable_ident]
            for lock in lock_list:
                if lock.transaction.identifier != transaction.identifier:
                    return false

            for lock in lock_list:
                if lock.transaction.identifier == transaction.identifier:
                    new_lock = lock
                    new_lock.lock_type = LockType.WRITE
                    lock_list[lock.index()] = new_lock
                    break
            
            locks[variable_ident] = lock_list
            return true


        

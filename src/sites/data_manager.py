# -*- coding: utf-8 -*-
""" Data Manager

This module represents the Data Manager, which manages all
Site specific data

"""
import copy
from src.objects.lock import Lock, LockType
from src.objects.transaction import TransactionType
from src.objects.variable import Variable

class DataManager:
    """ Maintains all data for a particular site """

    def __init__(self, variables):
        self.entries = {}
        self.variables = variables
        self.up_time = 0
        self.locks = {}

    def write_new_data(self, time, variable_ident, new_value, trans_identifier):
        """ Method to write the new value of the variable. This will go into the log """

        if trans_identifier not in self.entries:
            self.entries[trans_identifier] = {}
        
        if variable_ident not in self.entries[trans_identifier]:
            # update the new value of the variable
            
            new_variable = copy.copy(self.variables[variable_ident])
            new_variable.update_value(time, new_value)

            self.entries[trans_identifier][variable_ident] = new_variable

        else:
            self.entries[trans_identifier][variable_ident].update(time, new_value)

    def get_variable_value(self, identifier):
        """ Returns the last known committed value for this variable """

        return self.variables[identifier].value

    def get_value_at_time(self, variable, time, transaction):
        """ Returns the last known committed value for this variable """

        if transaction.trans_identifier in self.entries:
            if not time in self.entries[transaction.trans_identifier]:
                return self.get_value_at_time(variable, time-1, transaction)
            else:
                return self.entries[transaction.trans_identifier][time].value

    def obtain_write_lock(self, instruction, transaction):
        """ Obtain the Write Lock for a Transaction """

        lock_type = LockType.WRITE

        #get the variable from the variable identifier
        variable_ident = instruction.variable_identifier
        variable = self.variables[variable_ident]

        #Check if there are locks already for that variable
        if variable_ident not in self.locks: 
            lock = Lock(lock_type, transaction, variable)
            self.locks[variable_ident] = [lock]
            #TODO: log lock acquired 
            return None
        else:
            lock_list = self.locks[variable_ident]
            
            #If any transaction has a lock on the variable, this transaction cannot obtain a lock
            for lock in lock_list:
                if lock.transaction.identifier != transaction.identifier:
                    #TODO: log lock was not acquired
                    return lock.transaction.identifier

            #If the same transition has a lock, we just update the lock type
            #There should only be one lock for the variable in this case
            for idx, lock in enumerate(lock_list):
                if lock.transaction.identifier == transaction.identifier:
                    self.locks[variable_ident][idx].lock_type = LockType.WRITE
            #TODO: log lock updated and acquired
            return None

    def obtain_read_lock(self, transaction, instruction):
        """ Gets a read lock, if possible """

        variable = self.variables[instruction.variable_identifier]

        if not variable.readable:
            return False

        if transaction.transaction_type == TransactionType.READ_ONLY:
            return True

        if variable.identifier in self.locks:
            for lock in self.locks[variable.identifier]:
                if lock.transaction.index == transaction.index:
                    return True

            for lock in self.locks[variable.identifier]:
                if lock.lock_type == LockType.WRITE:
                    return False
        else:
            self.locks[variable.identifier] = []

        new_lock = Lock(LockType.READ, transaction, variable)
        self.locks[variable.identifier].append(new_lock)

        return True

    def get_write_lock_value(self, transaction, instruction):
        """ If a variable has a Write lock return the value of that write """

        if instruction.variable_identifier in self.locks:
            for lock in self.locks[instruction.variable_identifier]:
                if lock.lock_type == LockType.WRITE and lock.transaction.index == transaction.index:
                    return lock.variable.value

    def read(self, transaction, instruction):
        """ Gets the lated valued for this transaction """

        variable = self.variables[instruction.variable_identifier]

        write_value = self.get_write_lock_value(transaction, instruction)

        if not write_value:
            return variable.get_last_committed_value()

        return write_value

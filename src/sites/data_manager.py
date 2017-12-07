# -*- coding: utf-8 -*-
""" Data Manager

This module represents the Data Manager, which manages all
Site specific data

"""
import copy
from objects.lock import Lock, LockType
from objects.transaction import TransactionType
from objects.variable import Variable

class DataManager:
    """ Maintains all data for a particular site """

    def __init__(self, variables, logger, site_id):
        self.entries = {}
        self.variables = variables
        self.locks = {}
        self.logger = logger
        self.site_id = site_id

    def write_new_data(self, time, variable_ident, new_value, trans_identifier):
        """ Method to write the new value of the variable. This will go into the log """

        # TODO: Write a unit test to test a write when the site doesn't have that variable
        if variable_ident: 
            if trans_identifier not in self.entries:
                self.entries[trans_identifier] = {}

            if variable_ident not in self.entries[trans_identifier]:
                # update the new value of the variable

                new_variable = copy.copy(self.variables[variable_ident])
                new_variable.update_value(time, new_value)

                self.entries[trans_identifier][variable_ident] = new_variable
            else:
                self.entries[trans_identifier][variable_ident].update(time, new_value)
            last_committed_value = self.entries[trans_identifier][variable_ident].get_last_committed_value()
            self.logger.log("Site %s: Current Variable %s has been updated to %s by Transaction %s (if committed)" % \
                            (str(self.site_id), variable_ident, str(last_committed_value), trans_identifier))

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
            self.locks[variable_ident] = []
            lock = Lock(lock_type, transaction, variable)
            self.locks[variable_ident].append(lock)
            self.logger.log("Site %s: Acquired write lock for variable %s by Transaction %s" % \
                            (str(self.site_id), variable_ident, str(transaction.identifier)))
            return None
        else:
            lock_list = self.locks[variable_ident]

            #in case the locks are cleared, there would be an empty lock list
            if not lock_list:
                lock = Lock(lock_type, transaction, variable)
                self.locks[variable_ident].append(lock)
                self.logger.log("Site %s: Acquired write lock for variable %s by Transaction %s" %
                            (str(self.site_id), variable_ident, str(transaction.identifier)))
                return None
            else:
                #If any transaction has a lock on the variable, this transaction cannot obtain a lock
                for lock in lock_list:
                    if lock.transaction.identifier != transaction.identifier:
                        self.logger.log("Site %s: Failed to acquire write lock for variable %s by Transaction %s" %
                                        (str(self.site_id), variable_ident, str(transaction.identifier)))
                        return lock.transaction.identifier

                #If the same transition has a lock, we just update the lock type
                #There should only be one lock for the variable in this case
                for idx, lock in enumerate(lock_list):
                    if lock.transaction.identifier == transaction.identifier :
                        self.locks[variable_ident][idx].lock_type = LockType.WRITE
                self.logger.log("Site %s: Existing lock for variable %s was updated to a write lock by Transaction %s" % \
                                (str(self.site_id), variable_ident, str(transaction.identifier)))
                return None

    def obtain_read_lock(self, transaction, instruction):
        """ Gets a read lock, if possible """

        variable = self.variables[instruction.variable_identifier]

        if not variable.readable:
            self.logger.log("Site %s: Variable not readable, cannot obtain Read Lock for Variable %s by Transaction %s" %
                            (str(self.site_id), variable.identifier, str(transaction.identifier)))
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
        self.logger.log("Site %s: Read Lock acquired for Variable %s by Transaction %s" %
                        (str(self.site_id), variable.identifier, str(transaction.identifier)))
        return True

    def get_write_lock_value(self, transaction, instruction):
        """ If a variable has a Write lock return the value of that write """

        if instruction.variable_identifier in self.locks:
            for lock in self.locks[instruction.variable_identifier]:
                if lock.lock_type == LockType.WRITE and lock.transaction.index == transaction.index:
                    return self.entries[transaction.identifier][instruction.variable_identifier].get_last_committed_value()

    def get_write_lock_owner(self, instruction):
        if self.locks:
            for lock in self.locks[instruction.variable_identifier]:
                if lock.lock_type == LockType.WRITE:
                    return lock.transaction.identifier
        return None

    def read(self, transaction, instruction):
        """ Gets the lated valued for this transaction """

        variable = self.variables[instruction.variable_identifier]

        write_value = self.get_write_lock_value(transaction, instruction)

        if not write_value:
            return variable.get_last_committed_value()

        return write_value

    def commit(self, time, transaction):
        """ Commit variables """
        self.logger.log("Site %s: Attempting to commit Transaction %s" %
                        (str(self.site_id), str(transaction.identifier)))
        if transaction.identifier in self.entries:
            #self.logger.log("Entries: " + str(self.entries[transaction.identifier]))
            #self.logger.log("Locks before commit: " + str(self.locks))
            for variable_identifier, variable in self.entries[transaction.identifier].iteritems():
                if variable_identifier in self.locks:
                    for lock in self.locks[variable_identifier]:
                        #self.logger.log(str(lock))
                        if lock.lock_type == LockType.WRITE:
                            newest_value = variable.get_last_committed_value()
                            #self.logger.log("updated value: "+ str(newest_value))
                            self.variables[variable_identifier].update_value(time, newest_value)


        for variable_identifier in self.variables.keys():
            self.variables[variable_identifier].readable = True

        self.logger.log("Site %s: Successfully committed values for Transaction %s" %
                        (str(self.site_id), str(transaction.identifier)))
        #self.logger.log("Current variables: " + str(self.variables))
        self.clear_locks(transaction.identifier)

    def clear_locks(self, transaction_ident):
        """ Clear all locks """

        if self.locks:
            self.logger.log("Site %s: Clearing all locks for Transaction %s" % \
                            (str(self.site_id), transaction_ident))

            for variable_ident, lock_list in self.locks.iteritems():
                for lock in lock_list:
                    if lock.transaction.identifier == transaction_ident:
                        self.locks[variable_ident].remove(lock)


    def clear_entries(self, transaction_ident):
        """Clear the entries for the transaction_ident"""
        if self.entries:
            self.logger.log("Site %s: Clearing log entries for Transaction %s" % \
                            (str(self.site_id), transaction_ident))

            if transaction_ident in self.entries:
                del self.entries[transaction_ident]

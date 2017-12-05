# -*- coding: utf-8 -*-
""" Transaction Manager

This module represents the Transaction Manager, which manages
Transactions across all sites

"""
from objects.clock import Clock
from objects.instruction import InstructionType

class TransactionManager:
    """ Maintains all transactions for the database """

    def __init__(self, logger):
        self.logger = logger

    def execute(self, instruction):

        while instruction:
            if instruction.type == InstructionType.TRANSACTIONAL:
                # Case statement to process instruction
                pass
            else:
                # Call site execute method
                pass

        return "Process instruction"

    def begin_transaction(self):
        """ Begin a Transaction """
        pass

    def end_transaction(self):
        """ End a Transaction """
        pass

    def get(self):
        """ Get a Transaction """
        pass

    def commit(self):
        """ Commit a Transaction """
        pass

    def abort(self):
        """ Abort a Transaction """
        pass

    def read(self):
        """ Read the value of a Variable """
        pass

    def write(self):
        """ Write the value of a Variable """
        pass

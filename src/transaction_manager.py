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
        self.queue = []

    def execute(self, instruction):
        print "Executing transactional function"

    def begin_transaction(self):
        """ Begin a Transaction """
        print "Begin Transaction"

    def end_transaction(self):
        """ End a Transaction """
        print "End a Transaction"

    def get(self):
        """ Get a Transaction """
        print Get a Transaction

    def commit(self):
        """ Commit a Transaction """
        print "Commit a Transaction"

    def abort(self):
        """ Abort a Transaction """
        print "Abort a Transaction"

    def read(self):
        """ Read the value of a Variable """
        print Read the value of a Variable

    def write(self):
        """ Write the value of a Variable """
        print "Write the value of a Variable"

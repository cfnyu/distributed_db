# -*- coding: utf-8 -*-
""" Transaction Manager

This module represents the Transaction Manager, which manages
Transactions across all sites

"""
from objects.site import Site
from objects.instruction import InstructionType

class TransactionManager:
    """ Maintains all transactions for the database """

    def __init__(self, time, logger):
        self.logger = logger
        self.queue = {}
        self.sites = []

        # Python range function does not include last value so while there
        # Will only be 10 sites, the range must go to 11 to include 10
        for i in range(1, 11):
            site = Site(i, time, logger)
            self.sites.append(site)

        self.site_to_variables_map = { 1: ["x1", "x3"] }
        self.variables_to_site_map = { "x1": [1, 2] }

    def execute(self, instruction):
        """
        Reads instruction object and based on type it will call
        The appropriate method below or a site method

        """
        
        print "Executing transactional function"

    def begin_transaction(self):
        """ Begin a Transaction """
        print "Begin Transaction"

    def end_transaction(self):
        """ End a Transaction """
        print "End a Transaction"

    def get(self):
        """ Get a Transaction """
        print "Get a Transaction"

    def can_commit(self):
        """ Check if a transaction can be committed """
        print "Check if a transaction can be committed"

    def commit(self):
        """ Commit a Transaction """
        print "Commit a Transaction"

    def abort(self):
        """ Abort a Transaction """
        print "Abort a Transaction"

    def read(self):
        """ Read the value of a Variable """
        print "Read the value of a Variable"

    def write(self):
        """ Write the value of a Variable """
        print "Write the value of a Variable"

    def dump(self, args=None):
        # If args = #
        # Loop through all sites and call the dump method of individual site
        # Or call 
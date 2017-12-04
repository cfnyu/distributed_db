# -*- coding: utf-8 -*-
""" Transaction Manager

This module represents the Transaction Manager, which manages
Transactions across all sites

"""
from objects.site import Site
from objects.clock import Clock
from objects.instruction import InstructionType

class TransactionManager:
    """ Maintains all transactions for the database """

    def __init__(self, logger):
        self.sites = []
        self.clock = Clock()
        self.logger = logger

        # Python range function does not include last value so while there
        # Will only be 10 sites, the range must go to 11 to include 10
        for i in range(1, 11):
            site = Site(i, logger)
            self.sites.append(site)

    def execute(self, instruction):

        while instruction:
            if instruction.type == InstructionType.TRANSACTIONAL:
                # Case statement to process instruction
                pass
            else:
                # Call site execute method
                pass

        return "Process instruction"

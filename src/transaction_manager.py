# -*- coding: utf-8 -*-
""" Transaction Manager

This module represents the Transaction Manager, which manages
Transactions across all sites

"""
from src.objects.site import Site
from src.objects.instruction import InstructionType

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
        
        if instruction.instruction_type == InstructionType.BEGIN:
            self.begin_transaction(instruction)
        elif instruction.instruction_type == InstructionType.BEGIN_RO:
            self.begin_transaction(instruction)
        elif instruction.instruction_type == InstructionType.DUMP_ALL:
            self.dump(instruction)
        elif instruction.instruction_type == InstructionType.DUMP_SITE:
            self.dump(instruction)
        elif instruction.instruction_type == InstructionType.DUMP_VAR:
            self.dump(instruction)
        elif instruction.instruction_type == InstructionType.END:
            self.can_commit(instruction)
        elif instruction.instruction_type == InstructionType.FAIL:
            self.fail(instruction)
        elif instruction.instruction_type == InstructionType.READ:
            self.read(instruction)
        elif instruction.instruction_type == InstructionType.RECOVER:
            self.recover(instruction)
        elif instruction.instruction_type == InstructionType.WRITE:
            self.write(instruction)
        else:
            # Throw an exception
            pass

        print "Executing transactional function"

    def begin_transaction(self, instruction):
        """ Begin a Transaction """
        # Check Instruction type for either Readonly Transaction
        print "Begin Transaction"

    def end_transaction(self, instruction):
        """ End a Transaction """
        print "End a Transaction"

    def get(self, instruction):
        """ Get a Transaction """
        print "Get a Transaction"

    def can_commit(self, instruction):
        """ Check if a transaction can be committed """
        print "Check if a transaction can be committed"

    def commit(self, instruction):
        """ Commit a Transaction """
        print "Commit a Transaction"

    def abort(self, instruction):
        """ Abort a Transaction """
        print "Abort a Transaction"

    def read(self, instruction):
        """ Read the value of a Variable """
        print "Read the value of a Variable"

    def write(self, instruction):
        """ Write the value of a Variable """
        print "Write the value of a Variable"

    def dump(self, instruction):
        # If args = #
        # Loop through all sites and call the dump method of individual site
        # Or call 
        pass

    def fail(self, instruction):
        pass

    def recover(self, instruction):
        pass

# -*- coding: utf-8 -*-
""" Transaction Manager

This module represents the Transaction Manager, which manages
Transactions across all sites

"""
from src.objects.clock import Clock
from src.objects.site import Site
from src.objects.instruction import InstructionType
from src.objects.transaction import Transaction, TransactionType

class TransactionManager:
    """ Maintains all transactions for the database """

    def __init__(self, logger):
        self.logger = logger
        self.transactions = {}
        self.readonly_snapshots = {}
        self.sites = {}
        self.site_to_variables_map = {}
        self.variables_to_site_map = {}
        self.clock = Clock()

        # Python range function does not include last value so while there
        # Will only be 10 sites, the range must go to 11 to include 10
        for i in range(1, 11):
            site = Site(i, self.clock.time, logger)
            self.sites[site.identifer] = site
            self.site_to_variables_map[i] = site.data_manager.variables

            for variable in site.data_manager.variables:
                if variable not in self.variables_to_site_map:
                    self.variables_to_site_map[variable] = []

                self.variables_to_site_map[variable].append(site.identifer)

    def execute(self, instruction):
        """
        Reads instruction object and based on type it will call
        The appropriate method below or a site method

        """
        self.clock.tick()

        if instruction.instruction_type == InstructionType.BEGIN:
            return self.begin_transaction(instruction)
        elif instruction.instruction_type == InstructionType.BEGIN_RO:
            return self.begin_transaction(instruction)
        elif instruction.instruction_type == InstructionType.DUMP_ALL:
            return self.dump(instruction)
        elif instruction.instruction_type == InstructionType.DUMP_SITE:
            return self.dump(instruction)
        elif instruction.instruction_type == InstructionType.DUMP_VAR:
            return self.dump(instruction)
        elif instruction.instruction_type == InstructionType.END:
            return self.can_commit(instruction)
        elif instruction.instruction_type == InstructionType.FAIL:
            return self.fail(instruction)
        elif instruction.instruction_type == InstructionType.READ:
            return self.read(instruction)
        elif instruction.instruction_type == InstructionType.RECOVER:
            return self.recover(instruction)
        elif instruction.instruction_type == InstructionType.WRITE:
            return self.write(instruction)
        else:
            # Throw an exception
            pass

    def begin_transaction(self, instruction):
        """ Begin a Transaction """

        trans_ident = instruction.transaction_identifier

        if instruction.instruction_type == InstructionType.BEGIN:
            transaction = Transaction(trans_ident, TransactionType.READ_WRITE, \
                                      self.clock.time)
        else:
            # Take a snapshot of the data at the time of this transaction
            self.readonly_snapshots[trans_ident] = {}
            transaction = Transaction(trans_ident, TransactionType.READ_ONLY, self.clock.time)

            for site_identifier, site in self.sites.iteritems():
                for variable in site.data_manager.variables:
                    self.readonly_snapshots[trans_ident][site_identifier] = variable

        self.transactions[trans_ident] = transaction

    def end_transaction(self, instruction):
        """ End a Transaction """
        return "End a Transaction"

    def get(self, instruction):
        """ Get a Transaction """
        return "Get a Transaction"

    def can_commit(self, instruction):
        """ Check if a transaction can be committed """
        return "Check if a transaction can be committed"

    def commit(self, instruction):
        """ Commit a Transaction """
        return "Commit a Transaction"

    def abort(self, instruction):
        """ Abort a Transaction """
        return "Abort a Transaction"

    def read(self, instruction):
        """ Read the value of a Variable """
        return "Read the value of a Variable"

    def write(self, instruction):
        """ Write the value of a Variable """
        return "Write the value of a Variable"

    def dump(self, instruction):
        results = {}
        if instruction.site_identifier:
            results = self.sites[instruction.site_identifier].dump()
        elif instruction.variable_identifier:
            for ident, site in self.sites.iteritems():
                variable = instruction.variable_identifier
                if variable in site.data_manager.variables:
                    if ident not in results:
                        results[ident] = str(site.data_manager.variables[variable])
        else:
            results = {}
            for ident, site in self.sites.iteritems():
                results[ident] = site.dump()

        print results

    def fail(self, instruction):
        return "fail"

    def recover(self, instruction):
        return "recover"

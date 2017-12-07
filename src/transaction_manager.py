# -*- coding: utf-8 -*-
""" Transaction Manager

This module represents the Transaction Manager, which manages
Transactions across all sites

"""
from objects.clock import Clock
from objects.site import Site, SiteStatus
from objects.instruction import InstructionType
from objects.transaction import Transaction, TransactionType, TransactionState

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
        self.waiting_transactions_instructions_map = {}
        self.blocked_transactions_instructions_map = {}
        self.sites_transactions_accessed_log = {}

        # Python range function does not include last value so while there
        # Will only be 10 sites, the range must go to 11 to include 10
        for i in range(1, 11):
            site = Site(i, self.clock.time, logger)
            self.sites[site.identifer] = site
            self.site_to_variables_map[site.identifer] = site.data_manager.variables

            for var_id, variable in site.data_manager.variables.iteritems():
                if variable.identifier not in self.variables_to_site_map:
                    self.variables_to_site_map[variable.identifier] = []

                self.variables_to_site_map[variable.identifier].append(site.identifer)

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
                if site.status == SiteStatus.UP:
                    for variable in site.data_manager.variables:
                        if site_identifier not in self.readonly_snapshots[trans_ident]:
                            self.readonly_snapshots[trans_ident][site_identifier] = []
                        self.readonly_snapshots[trans_ident][site_identifier].append(variable)

        self.transactions[trans_ident] = transaction

    def end_transaction(self, transaction):
        """ End a Transaction """

        if transaction.transaction_type == TransactionType.READ_ONLY:
            # If a site is down add this task to the waiting transactions
            for site in self.sites_transactions_accessed_log[transaction.identifier]:
                if site.status != SiteStatus.UP:
                    # TODO: Confirm that this cannot occur with the professor
                    raise ArithmeticError("You are trying to end a transaction before recovering a site that went down")

        can_commit = False
        for site_id, access_time in self.sites_transactions_accessed_log[transaction.identifier].iteritems():
            site = self.sites[site_id]

            can_commit = (site.status == SiteStatus.UP and site.create_time == access_time)

            if not can_commit:
                break

        transaction.end_time = self.clock.time
        if transaction.transaction_type == TransactionType.READ_ONLY or can_commit:
            for site_id, access_time in self.sites_transactions_accessed_log[transaction.identifier].iteritems():
                site = self.sites[site_id]
                site.data_manager.commit(self.clock.time, transaction)
                site.data_manager.clear_locks(transaction)

            self.sites_transactions_accessed_log.pop(transaction.identifier, None)
            self.transactions.pop(transaction.identifier, None)

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

        if instruction.transaction_identifier not in self.transactions:
            raise ValueError("Transaction %s was never started" % \
                             instruction.transaction_identifier)

        transaction = self.transactions[instruction.transaction_identifier]
        possible_sites_ids = self.variables_to_site_map[instruction.variable_identifier]
        possible_sites = len(possible_sites_ids)

        if possible_sites == 0:
            # TODO: Store transaction in the waiting bucket
            pass
        else:
            for site_id in possible_sites_ids:
                site = self.sites[site_id]
                if site.status == SiteStatus.UP:
                    if transaction.transaction_type == TransactionType.READ_ONLY:
                        if site_id in self.readonly_snapshots[transaction.identifier]:
                            return self.readonly_snapshots[transaction.identifier][site_id]
                    else:
                        if site.data_manager.obtain_read_lock(transaction, instruction):
                            value = site.data_manager.read(transaction, instruction)
                            if transaction.identifier not in self.sites_transactions_accessed_log:
                                self.sites_transactions_accessed_log[transaction.identifier] = {}

                            self.sites_transactions_accessed_log[transaction.identifier][site_id] = self.clock.time

                            print "%s: %s at site %s" % \
                                (instruction.variable_identifier, str(value), str(site_id))

        return "Read the value of a Variable"

    def write(self, instruction):
        """ Write the value of a Variable """

        #get the transaction identifier from the instruction
        transaction_ident = instruction.transaction_identifier

        #check if the transaction is active (i.e. if it is not aborted or committed)
        transaction = self.transactions[transaction_ident]
        if transaction:
            if transaction.state == TransactionState.ABORTED:
                #TODO: log that transaction was aborted, couldn't write
                return
            else:
                stable_sites = []
                sites_with_variable = self.variables_to_site_map[instruction.variable_identifier]

                for site_id in sites_with_variable:
                    #get the site object from the sites list
                    site = self.sites[site_id]
                    if site.status == SiteStatus.UP:
                        stable_sites.append(site)
                
                site_count = len(stable_sites)
                if site_count == 0:  #No available site
                    transaction.state = TransactionState.WAITING
                    self.transactions[transaction_ident] = transaction
                    self.waiting_transactions_instructions_map[transaction_ident] = instruction
                else:
                    # Check if this instruction was in waiting map
                    if transaction_ident in self.waiting_transactions_instructions_map:
                        del self.waiting_transactions_instructions_map[transaction_ident]
                        transaction.state = TransactionState.RUNNING
                        self.transactions[transaction_ident] = transaction

                    is_transaction_blocked = False
                    for site in stable_sites:
                        # This checks if lock can be obtained on the available site,
                        # If lock can be obtained None is returned, and if not, 
                        # Returns the blocking transaction identifier

                        blocked_transaction_id = self.sites[site.identifer].data_manager.obtain_write_lock(instruction, transaction)
                        # If transaction is blocked, then append in the blocked instructions table and then break
                        if blocked_transaction_id:
                            if blocked_transaction_id not in self.blocked_transactions_instructions_map:
                                self.blocked_transactions_instructions_map[blocked_transaction_id] = instruction
                            else:
                                self.blocked_transactions_instructions_map[blocked_transaction_id].append(instruction)
                            is_transaction_blocked = True
                        break

                    if is_transaction_blocked:
                        transaction.state = TransactionState.BLOCKED
                        self.transactions[transaction_ident] = transaction
                        #checkForDeadlock
                    else:
                        #remove instruction from blocked_transaction_instructions_map if present
                        for blocked_transaction_id in self.blocked_transactions_instructions_map:
                            if instruction in self.blocked_transactions_instructions_map[blocked_transaction_id]:
                                self.blocked_transactions_instructions_map[blocked_transaction_id].remove(instruction)
                        
                        if transaction.state != TransactionState.RUNNING:
                            transaction.state = TransactionState.RUNNING
                            self.transactions[transaction_ident] = transaction

                        #do the actual updating here       
                        for site in stable_sites:
                            if instruction.variable_identifier in self.sites[site.identifer].variables:
                                self.sites[site.identifer].data_manager.write_new_data( \
                                    self.clock.time, instruction.variable_identifier, \
                                    instruction.value, instruction.transaction_identifier)

                                #TODO: log/print that write successful provided commit happens
                                
                                #add the sites the value was written to by the transaction in a dictionary
                                #This will be used to abort the transaction when any of the stable_sites fail
                                if transaction_ident not in self.sites_transactions_accessed_log:
                                    self.sites_transactions_accessed_log[transaction_ident] = {}
                                
                                self.sites_transactions_accessed_log[transaction_ident][site.identifer] = self.clock.time
                                #     set(stable_sites)
                                # else:
                                #     sites_set = self.sites_transactions_accessed_log[transaction_ident]
                                #     self.sites_transactions_accessed_log[transaction_ident] = sites_set.union(set(stable_sites))

    def dump(self, instruction):
        """ Prints out variable values to stdout """

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



# -*- coding: utf-8 -*-
""" Transaction Manager

This module represents the Transaction Manager, which manages
Transactions across all sites

"""
from src.objects.clock import Clock
from src.objects.site import Site, SiteStatus
from src.objects.instruction import InstructionType
from src.objects.transaction import Transaction, TransactionType, TransactionState

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
            self.site_to_variables_map[i] = site.data_manager.variables

            for variable in site.data_manager.variables:
                if variable not in self.variables_to_site_map:
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
                for variable in site.data_manager.variables:
                    #Todo: make a list here
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
                
                if len(stable_sites) == 0:  #No available site
                    transaction.state = TransactionState.WAITING
                    self.transactions[transaction_ident] = transaction
                    self.waiting_transactions_instructions_map[transaction_ident] = instruction
                else:
                    #check if this instruction was in waiting map
                    if transaction_ident in self.waiting_transactions_instructions_map:
                        del self.waiting_transactions_instructions_map[transaction_ident]
                        transaction.state = TransactionState.RUNNING
                        self.transactions[transaction_ident] = transaction
                    
                    is_transaction_blocked = False
                    for site in stable_sites:
                        #this checks if lock can be obtained on the available site, 
                        # if lock can be obtained None is returned, and if not, returns the blocking transaction identifier
                        blocked_transaction_id = self.sites[site.identifer].data_manager.obtain_write_lock(instruction, transaction)
                        #if transaction is blocked, then append in the blocked instructions table and then break
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
                            self.sites[site.identifer].data_manager.write_new_data(
                                self.clock.time, instruction.variable_identifier, instruction.value, instruction.transaction_identifier)
                            #TODO: log/print that write successful provided commit happens
                            
                        #add the sites the value was written to by the transaction in a dictionary
                        #This will be used to abort the transaction when any of the stable_sites fail
                        if transaction_ident not in self.sites_transactions_accessed_log:
                            self.sites_transactions_accessed_log[transaction_ident] = set(stable_sites)
                        else:
                            sites_set = self.sites_transactions_accessed_log[transaction_ident]
                            self.sites_transactions_accessed_log[transaction_ident] = sites_set.union(set(stable_sites))



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



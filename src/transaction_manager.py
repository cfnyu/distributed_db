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
            return self.end_transaction(self.transactions[instruction.transaction_identifier])
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

        if transaction.state == TransactionState.ABORTED:
            print "Transaction %s has already aborted" % transaction.identifier
            return False

        if transaction.transaction_type == TransactionType.READ_ONLY:
            self.transactions[transaction.identifier].end_time = self.clock.time
            self.transactions[transaction.identifier].state = TransactionState.COMMITTED
            print transaction.identifier, "committed/ended"
            del self.readonly_snapshots[transaction.identifier]
            return True

        self.commit(transaction)

        if transaction.identifier in self.sites_transactions_accessed_log:
            del self.sites_transactions_accessed_log[transaction.identifier]
        
    def commit(self, transaction):
        """ Commit a Transaction """
        
        self.transactions[transaction.identifier].end_time = self.clock.time
        self.transactions[transaction.identifier].state = TransactionState.COMMITTED

        if transaction.identifier in self.sites_transactions_accessed_log:

            for site in self.sites_transactions_accessed_log[transaction.identifier]:
                self.sites[site.identifer].data_manager.commit(self.clock.time, transaction)
                self.sites[site.identifer].data_manager.clear_locks(transaction)
        
        print transaction.identifier, "committed/ended"

        blocked_instructions_list = []

        if transaction.identifier in self.blocked_transactions_instructions_map:
            blocked_instructions_list = self.blocked_transactions_instructions_map[transaction.identifier]
            del self.blocked_transactions_instructions_map[transaction.identifier]

        if blocked_instructions_list:
            self.rerun(blocked_instructions_list)

    def abort(self, instruction):
        """ Abort a Transaction """
        return "Abort a Transaction"

    def rerun(self, instructions=None):
        # Change status of transaction to Running from Block
        # Check if this instruction was in waiting map
        # Loop through all transactions
        # if transaction_ident in self.waiting_transactions_instructions_map:
        #     del self.waiting_transactions_instructions_map[transaction_ident]
        #     transaction.state = TransactionState.RUNNING
        #     self.transactions[transaction_ident] = transaction
        pass

    def read(self, instruction):
        """ Read the value of a Variable """

        if instruction.transaction_identifier not in self.transactions:
            raise ValueError("Transaction %s was never started" % \
                             instruction.transaction_identifier)

        transaction = self.transactions[instruction.transaction_identifier]
        possible_sites_ids = self.variables_to_site_map[instruction.variable_identifier]
        possible_sites = len(possible_sites_ids)
        obtained_lock = False
        first_available_site_id = None

        if possible_sites == 0:
            transaction.state = TransactionState.WAITING
            self.transactions[transaction.identifier] = transaction
            self.waiting_transactions_instructions_map[transaction.identifier] = instruction
        else:
            for site_id in possible_sites_ids:
                site = self.sites[site_id]
                if site.status == SiteStatus.UP:
                    if transaction.transaction_type == TransactionType.READ_ONLY:
                        if site_id in self.readonly_snapshots[transaction.identifier]:
                            return self.readonly_snapshots[transaction.identifier][site_id]
                    else:
                        obtained_lock = site.data_manager.obtain_read_lock(transaction, instruction)
                        if not obtained_lock:
                            transaction_lock_owner = site.data_manager.get_write_lock_owner(instruction)

                            # If transaction is blocked, then append in the blocked instructions table and then break
                            if transaction_lock_owner:
                                if transaction_lock_owner not in self.blocked_transactions_instructions_map:
                                    self.blocked_transactions_instructions_map[transaction_lock_owner] = instruction
                                else:
                                    self.blocked_transactions_instructions_map[transaction_lock_owner].append(instruction)
                                self.transactions[transaction.identifier].state == TransactionState.BLOCKED
                            break

                        if transaction.identifier not in self.sites_transactions_accessed_log:
                            self.sites_transactions_accessed_log[transaction.identifier] = set()
                    
                        self.sites_transactions_accessed_log[transaction.identifier].add(site)

                        if not first_available_site_id:
                            first_available_site_id = site_id

            if obtained_lock:
                value = self.sites[first_available_site_id].data_manager.read(transaction, instruction)

                print "%s: %s at site %s" % (instruction.variable_identifier, str(value), str(first_available_site_id))

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
                        #do the actual updating here       
                        for site in stable_sites:
                            self.sites[site.identifer].data_manager.write_new_data( \
                                self.clock.time, instruction.variable_identifier, \
                                instruction.value, instruction.transaction_identifier)

                                #TODO: log/print that write successful provided commit happens
                                
                        #add the sites the value was written to by the transaction in a dictionary
                        #This will be used to abort the transaction when any of the stable_sites fail
                        if transaction_ident not in self.sites_transactions_accessed_log:
                            self.sites_transactions_accessed_log[transaction_ident] = set(stable_sites)
                        else:
                            sites_set = self.sites_transactions_accessed_log[transaction_ident]
                            self.sites_transactions_accessed_log[transaction_ident] = sites_set.union(set(stable_sites))

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
        """Fails the site and aborts transaction that accessed (performed read or write operation) the site """

        site_index = instruction.site_identifier
        self.sites[site_index].fail()

        print "Site " + str(site_index) + " has failed."

        transactions_to_abort = []
        for trans_ident in self.sites_transactions_accessed_log:
            if self.transactions[trans_ident].state != TransactionState.COMMITTED:
                sites_list = self.sites_transactions_accessed_log[trans_ident]
                for site in sites_list:
                    if site.identifer == site_index:
                        transactions_to_abort.append(trans_ident)
        
        #if transactions_to_abort:
           # for trans_id in transactions_to_abort:
               # self.abort_transaction(trans_id, site_index)

    def recover(self, instruction):
        return "recover"


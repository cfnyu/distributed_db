# -*- coding: utf-8 -*-
""" Transaction Manager

This module represents the Transaction Manager, which manages
Transactions across all sites

"""
import pprint
import copy
from objects.clock import Clock
from objects.site import Site, SiteStatus
from objects.instruction import InstructionType
from objects.transaction import Transaction, TransactionType, TransactionState
from objects.variable import Variable

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
        self.sites_transactions_read_write_log = {}

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
        self.logger.log("At clock tick : " + str(self.clock.time))
        self.rerun()

        if instruction.instruction_type == InstructionType.BEGIN or \
           instruction.instruction_type == InstructionType.BEGIN_RO:
            return self.begin_transaction(instruction)
        elif instruction.instruction_type == InstructionType.DUMP_ALL or \
             instruction.instruction_type == InstructionType.DUMP_SITE or \
             instruction.instruction_type == InstructionType.DUMP_VAR:
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
            self.logger.log("Starting RW transaction %s" % \
                            instruction.transaction_identifier)
        else:
            self.logger.log("Starting Read-Only transaction %s" % \
                            instruction.transaction_identifier)
            # Take a snapshot of the data at the time of this transaction
            self.readonly_snapshots[trans_ident] = {}
            transaction = Transaction(trans_ident, TransactionType.READ_ONLY, self.clock.time)

            for site_identifier, site in self.sites.iteritems():
                if site.status == SiteStatus.UP:
                    for variable_identifier, variable in site.data_manager.variables.iteritems():
                        # print variable, "On site", site_identifier
                        if variable.readable:
                            if site_identifier not in self.readonly_snapshots[trans_ident]:
                                self.readonly_snapshots[trans_ident][site_identifier] = []
                            
                            current_variable = Variable(self.clock.time, int(variable_identifier.replace("x", "")))
                            self.readonly_snapshots[trans_ident][site_identifier].append(current_variable)
            
            self.logger.log("Snapshot taken for RO Transaction %s")

        self.transactions[trans_ident] = transaction

    def end_transaction(self, transaction):
        """ End a Transaction """

        self.logger.log("Attempting to end transaction %s" % transaction.identifier)

        if transaction.state == TransactionState.ABORTED:
            self.logger.log("Transaction %s cannot be ended because it has already aborted" % transaction.identifier)
            return False

        if transaction.transaction_type == TransactionType.READ_ONLY:
            self.transactions[transaction.identifier].end_time = self.clock.time
            self.transactions[transaction.identifier].state = TransactionState.COMMITTED
            print transaction.identifier, "committed"
            del self.readonly_snapshots[transaction.identifier]
            self.logger.log("RO Transaction %s committed" % transaction.identifier)
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
                if self.sites[site.identifer].status == SiteStatus.UP:
                    self.sites[site.identifer].data_manager.commit(self.clock.time, transaction)

        output = "RW Transaction %s committed successfully" % transaction.identifier
        print output
        self.logger.log(output)

        blocked_instructions_list = []

        if transaction.identifier in self.blocked_transactions_instructions_map:
            blocked_instructions_list = self.blocked_transactions_instructions_map[transaction.identifier]
            del self.blocked_transactions_instructions_map[transaction.identifier]

        if blocked_instructions_list:
            self.rerun(blocked_instructions_list)

    def abort(self, transaction_ident, site_index=None):
        """ Abort a Transaction """

        self.logger.log("Attempting to abort transaction %s" % transaction_ident)
        self.transactions[transaction_ident].state = TransactionState.ABORTED
        self.transactions[transaction_ident].end_time = self.clock.time

        if transaction_ident in self.sites_transactions_accessed_log:
            for site in self.sites_transactions_accessed_log[transaction_ident]:
                self.sites[site.identifer].data_manager.clear_locks(transaction_ident)
                self.sites[site.identifer].data_manager.clear_entries(transaction_ident)
            del self.sites_transactions_accessed_log[transaction_ident]

        if transaction_ident in self.waiting_transactions_instructions_map:
            del self.waiting_transactions_instructions_map[transaction_ident]

        blocked_instructions_list = []
        if transaction_ident in self.blocked_transactions_instructions_map:
            blocked_instructions_list = self.blocked_transactions_instructions_map[transaction_ident]
            del self.blocked_transactions_instructions_map[transaction_ident]

        if site_index:
            self.logger.log("Transaction %s was aborted because it performed read or write operation on failed site %s." % \
                            (transaction_ident, str(site_index)))
            print "Transaction %s was aborted because it performed read or write operation on failed site %s." % \
                (transaction_ident, str(site_index))
        else:
            self.logger.log("Transaction %s was aborted because deadlock was detected." % transaction_ident)
            print "Transaction %s was aborted because deadlock was detected." % transaction_ident

        if blocked_instructions_list:
            self.rerun(blocked_instructions_list)

    def rerun(self, instructions=None):
        """ Rerun waiting/blocked transactions """

        self.logger.log("Attempting to rerun Waiting/Blocked transactions")

        if len(self.waiting_transactions_instructions_map) == 0:
            self.logger.log("No waiting transaction to rerun.")
        else:
            for transaction_ident, instruction in self.waiting_transactions_instructions_map.iteritems():
                del self.waiting_transactions_instructions_map[transaction_ident]
                self.logger.log("Rerunning transaction: " + transaction_ident)
                self.transactions[transaction_ident].state = TransactionState.RUNNING
                self.execute(instruction)

        if instructions:
            for instruction in instructions:
                if(self.transactions[instruction.transaction_identifier].state != TransactionState.ABORTED):
                    self.logger.log("Rerunning transaction: " + instruction.transaction_identifier)
                    self.transactions[instruction.transaction_identifier].state = TransactionState.RUNNING
                    self.execute(instruction)
                else:
                    self.logger.log("Couldn't rerun transaction: " + instruction.transaction_identifier + " because it was aborted.")

    def read(self, instruction):
        """ Read the value of a Variable """

        if instruction.transaction_identifier not in self.transactions:
            raise ValueError("Transaction %s was never started" % \
                             instruction.transaction_identifier)

        transaction = self.transactions[instruction.transaction_identifier]
        if transaction.state == TransactionState.ABORTED:
            self.logger.log("Read rejected, Transaction %s was already aborted" %
                            transaction.identifier)
            return
        possible_sites_ids = self.variables_to_site_map[instruction.variable_identifier]
        possible_sites = len(possible_sites_ids)
        obtained_lock = False
        first_available_site_id = None

        stable_sites = []
        sites_with_variable = self.variables_to_site_map[instruction.variable_identifier]

        for site_id in sites_with_variable:
            #get the site object from the sites list
            site = self.sites[site_id]
            if site.status == SiteStatus.UP:
                stable_sites.append(site)
        
        possible_sites = len(stable_sites)

        if possible_sites == 0:
            self.logger.log("No sites available for read")
            transaction.state = TransactionState.WAITING
            self.transactions[transaction.identifier] = transaction
            self.waiting_transactions_instructions_map[transaction.identifier] = instruction
        else:
            self.logger.log("%i site is available for read" % possible_sites)
            for site in stable_sites:
                if transaction.transaction_type == TransactionType.READ_ONLY:
                    if site.identifer in self.readonly_snapshots[transaction.identifier]:
                        for variable in self.readonly_snapshots[transaction.identifier][site.identifer]:
                            if variable.identifier == instruction.variable_identifier:
                                print "Read %s: %s at site %s" % (variable.identifier, variable.value, site.identifer)
                                return
                else:
                    obtained_lock = site.data_manager.obtain_read_lock(transaction, instruction)
                    if not obtained_lock:
                        transaction_lock_owner = site.data_manager.get_write_lock_owner(instruction)

                        # If transaction is blocked, then append in the blocked instructions table and then break
                        if transaction_lock_owner:
                            if transaction_lock_owner not in self.blocked_transactions_instructions_map:
                                self.blocked_transactions_instructions_map[transaction_lock_owner] = [instruction]
                            else:
                                self.blocked_transactions_instructions_map[transaction_lock_owner].append(instruction)
                            self.transactions[transaction.identifier].state == TransactionState.BLOCKED
                        break

                    if transaction.identifier not in self.sites_transactions_accessed_log:
                        self.sites_transactions_accessed_log[transaction.identifier] = set()
                
                    self.sites_transactions_accessed_log[transaction.identifier].add(site)

                    if not first_available_site_id:
                        first_available_site_id = site.identifer

            if obtained_lock:
                value = self.sites[first_available_site_id].data_manager.read(transaction, instruction)
                if not transaction.identifier in self.sites_transactions_read_write_log:
                    self.sites_transactions_read_write_log[transaction.identifier] = []

                self.sites_transactions_read_write_log[transaction.identifier].append(first_available_site_id)

                print "%s: Read %s - value %s at site %s" % (instruction.transaction_identifier, instruction.variable_identifier, str(value), str(first_available_site_id))
            else:
                self.check_for_deadlock()

    def write(self, instruction):
        """ Write the value of a Variable """

        #get the transaction identifier from the instruction
        transaction_ident = instruction.transaction_identifier

        #check if the transaction is active (i.e. if it is not aborted or committed)
        transaction = self.transactions[transaction_ident]
        if transaction:
            if transaction.state == TransactionState.ABORTED:
                self.logger.log("Write rejected, Transaction %s was already aborted" % \
                                transaction_ident)
                return

            stable_sites = []
            sites_with_variable = self.variables_to_site_map[instruction.variable_identifier]

            for site_id in sites_with_variable:
                #get the site object from the sites list
                site = self.sites[site_id]
                if site.status == SiteStatus.UP:
                    stable_sites.append(site)

            site_count = len(stable_sites)
            if site_count == 0:  #No available site
                self.logger.log("No available sites found, Transaction %s has been added to the wait queue" % \
                                transaction_ident)
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
                        self.logger.log("A write lock could not be obtained, Transaction %s has been added to the blocked queue" % \
                                transaction_ident)

                        if blocked_transaction_id not in self.blocked_transactions_instructions_map:
                            self.blocked_transactions_instructions_map[blocked_transaction_id] = [instruction]
                        else:
                            self.blocked_transactions_instructions_map[blocked_transaction_id].append(instruction)
                        is_transaction_blocked = True
                        break

                if is_transaction_blocked:
                    self.transactions[transaction_ident].state = TransactionState.BLOCKED
                    #check for deadlock
                    self.check_for_deadlock()
                else:
                    for site in stable_sites:
                        self.sites[site.identifer].data_manager.write_new_data( \
                            self.clock.time, instruction.variable_identifier, \
                            instruction.value, instruction.transaction_identifier)
                        self.logger.log("Variable %s updated in site %i with value %s by Transaction %s, provided transaction commits." % \
                                    (instruction.variable_identifier, site.identifer, str(instruction.value), instruction.transaction_identifier))
                        
                        if not transaction_ident in self.sites_transactions_read_write_log:
                            self.sites_transactions_read_write_log[transaction_ident] = []

                        self.sites_transactions_read_write_log[transaction.identifier].append(site.identifer)

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

        pprint.pprint(results)

    def fail(self, instruction):
        """Fails the site and aborts transaction that accessed
        (performed read or write operation) the site
        """

        self.logger.log("Failing site %s" % str(instruction.site_identifier))

        site_index = instruction.site_identifier
        self.sites[site_index].fail()

        self.logger.log("Site " + str(site_index) + " has failed.")

        transactions_to_abort = []
        for trans_ident in self.sites_transactions_accessed_log:
            if self.transactions[trans_ident].state != TransactionState.COMMITTED:
                sites_list = self.sites_transactions_accessed_log[trans_ident]
                for site in sites_list:
                    if site.identifer == site_index and \
                        self.sites_transactions_read_write_log[trans_ident] == site_index:
                        transactions_to_abort.append(trans_ident)

        if transactions_to_abort:
            for trans_id in transactions_to_abort:
                self.abort(trans_id, site_index)

    def recover(self, instruction):
        """ Recover a site from failure """

        self.logger.log("Recovering site %s" % str(instruction.site_identifier))

        site_index = instruction.site_identifier
        self.sites[site_index].recover(self.clock.time)

        self.logger.log("Site " + str(site_index) + " has recovered.")

    def check_for_deadlock(self):
        """Check for deadlock and abort the youngest transaction"""
        self.logger.log("Checking for deadlock.")

        active_transactions_list = []
        for trans_id in self.transactions:
            if self.transactions[trans_id].state != TransactionState.ABORTED and \
                self.transactions[trans_id].state != TransactionState.COMMITTED:
                active_transactions_list.append(self.transactions[trans_id])

        #create a transaction_graph
        transaction_graph = self.create_graph(active_transactions_list)
        self.logger.log("Transaction graph: " + str(transaction_graph))

        #check for cycles in the transaction_graph
        visited_set = set()
        done_set = set()
        has_cycle = False

        for vertex in transaction_graph:
            if vertex not in visited_set and not has_cycle:
                has_cycle = self.dfs_check_cycle(vertex, transaction_graph, visited_set, done_set)

        if not has_cycle:
            self.logger.log("Cycle not detected, no deadlock.")
        else:
            self.logger.log("Cycle detected, there is a deadlock.")
            transaction_id_to_abort = self.get_transaction_id_to_kill(visited_set)
            self.logger.log("Youngest transaction id: " + transaction_id_to_abort + ". Will be aborted.")
            self.abort(transaction_id_to_abort)


    def create_graph(self, active_transactions_list):
        """ Create a transaction graph
        This should create a graph of {transaction1: [list of transactions that transaction1 is waiting to finish ]}
        """
        transaction_graph = {}

        if active_transactions_list:
            #locked_variables_to_transactions_map = get_locked_variables_to_transactions_map(sites)
            for active_transaction in active_transactions_list:
                transaction_graph[active_transaction.identifier] = []

                #check if transaction is blocked
                if active_transaction.state == TransactionState.BLOCKED:
                    blocked_trans_set = set()
                    #get the blocked_instruction from the list value of blocked_transactions_instructions_map
                    for blocking_trans_id, blocked_instructions_list in self.blocked_transactions_instructions_map.iteritems():
                        for blocked_instruction in blocked_instructions_list:
                            if blocked_instruction.transaction_identifier == active_transaction.identifier:
                                #if the transaction in blocked instruction list is equal to the current blocked transaction
                                #get the transaction that is blocking it
                                blocked_trans_set.add(blocking_trans_id)
                    transaction_graph[active_transaction.identifier] = list(blocked_trans_set)

        return transaction_graph

    def dfs_check_cycle(self, vertex, graph, visited_set, done_set):
        visited_set.add(vertex)
        if vertex in graph:
            for neighbour in graph[vertex]:
                if neighbour not in visited_set and neighbour not in done_set:
                    self.dfs_check_cycle(neighbour, graph, visited_set, done_set)

                if neighbour in visited_set and neighbour not in done_set:
                    return True
        done_set.add(vertex)
        return False

    def get_transaction_id_to_kill(self, visited_set):
        max_start_time = -1
        max_trans_ident = ""
        if visited_set:
            for trans_id in visited_set:
                if self.transactions[trans_id].start_time > max_start_time:
                    max_start_time = self.transactions[trans_id].start_time
                    max_trans_ident = trans_id

        return max_trans_ident

# -*- coding: utf-8 -*-
""" Transaction

This module represents a single transaction object

"""
from enum import Enum

class TransactionState(Enum):
    """ Represents the Transaction State """
    ABORTED = 1, # When a transaction is killed before it is ended
    BLOCK = 2, # If the transaction is waiting for a lock to be released
    COMMITTED = 3,
    RUNNING = 4,
    WAITING = 5 # Waiting for an available site 

class TransactionType(Enum):
    """ Represents the Transaction Type """
    READ_ONLY = 1,
    READ_WRITE = 2

class Transaction:
    def __init__(self, identifier, transaction_type, start_time):
        self.index = identifier # Extract number from identifier
        self.identifier = identifier
        self.transaction_type = transaction_type
        self.start_time = start_time
        self.end_time = None
        # Wait time?
        # Buffer

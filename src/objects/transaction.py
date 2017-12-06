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
    """ Represents a single transaction object """

    def __init__(self, identifier, transaction_type, start_time):
        self.index = int(identifier.upper().replace("T", ""))
        self.identifier = identifier
        self.transaction_type = transaction_type
        self.start_time = start_time
        self.end_time = None
        self.state = TransactionState.WAITING
        # Wait time?
        # Buffer

# -*- coding: utf-8 -*-
""" Lock

This module represents a single Lock

"""
from enum import IntEnum

class LockType(IntEnum):
    """ Represents the Lock Type """
    READ = 1,
    WRITE = 2

class Lock:
    """ Represents a single Lock object """

    def __init__(self, lock_type, transaction, variable):
        self.lock_type = lock_type
        self.transaction = transaction
        self.variable = variable

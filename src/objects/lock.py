# -*- coding: utf-8 -*-
""" Lock

This module represents a single Lock

"""
from enum import Enum

class LockType(Enum):
    """ Represents the Lock Type """
    READ = 1,
    WRITE = 2

class Lock:
    
    def __init__(self, type, transaction, variable):
        self.type = type
        self.transaction = transaction
        self.variable = variable
# -*- coding: utf-8 -*-
""" Instruction

This module represents a single instruction

"""
from enum import Enum

class InstructionType(Enum):
    """ Represents the Instruction Type """
    BEGIN = 1,
    BEGIN_RO = 2,
    READ = 3,
    WRITE = 4,
    DUMP = 5,
    END = 6,
    FAIL = 7,
    RECOVER = 8

class Instruction:
    """ This class represents an instruction """

    def __init__(self, time, instruction_str):
        # TODO: Parse the instruction
        self.variable_type = InstructionType.SITE
        self.variable_identifier = None
        self.site = None
        self.transaction = None

        if any(val in instruction_str for val in ['Dump', 'Fail', 'Recover']):
            self.site = 1 # Site to access
        else:
            self.transaction = "Create transaction" # Transaction(time)
            if self.variable_type == InstructionType.READ or self.variable_type == InstructionType.WRITE:
                self.variable_identifier = "x1"

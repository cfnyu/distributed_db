# -*- coding: utf-8 -*-
""" Instruction

This module represents a single instruction

"""
# INSTRUCTION_TYPES = ['Begin', 'BeginRO', 'Read', 'Write', 'Dump', 'End', 'Fail', 'Recover']
# INSTRUCTION_TYPES = ['transaction', 'site']
from enum import Enum

class InstructionType(Enum):
    """ Represents the type of instruction """
    TRANSACTIONAL = 1
    SITE = 2

class Instruction:
    """ This class represents an instruction """

    def __init__(self, instruction):

        if any(val in instruction for val in ['Dump', 'Fail', 'Recover']):
            self.type = InstructionType.SITE
        else:
            self.type = InstructionType.TRANSACTIONAL

        self.instruction = instruction

    def __repr__(self):
        return "<Instruction (%s): %s" % (self.type, self.instruction)

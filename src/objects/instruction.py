# -*- coding: utf-8 -*-
""" Instruction

This module represents a single instruction

"""
import re
from enum import IntEnum

TRANSACTION_EXPR = "\s*(t[1-9]|t10)\s*"
VARIABLE_EXPR = "\s*(x[1-9]{1}|x1[1-9]{1}|x10|x20)\s*"
SITE_EXPR = "\s*([1-9]|10)\s*"

class InstructionType(IntEnum):
    """ Represents the Instruction Type """
    BEGIN = 1,
    BEGIN_RO = 2,
    DUMP_ALL = 3,
    DUMP_SITE = 4,
    DUMP_VAR = 5,
    END = 6,
    FAIL = 7,
    READ = 8,
    RECOVER = 9,
    WRITE = 10

class Instruction:
    """ This class represents an instruction """

    def __init__(self, instruction_str):
        self.instruction_type = self.get_type(instruction_str)
        self.variable_identifier = None
        self.site_identifier = None
        self.transaction_identifier = None
        self.value = None

        if self.instruction_type == InstructionType.BEGIN or \
           self.instruction_type == InstructionType.BEGIN_RO or \
           self.instruction_type == InstructionType.END:
            self.transaction_identifier = self.get_single_value(instruction_str).strip()
        elif self.instruction_type == InstructionType.READ:
            values = self.get_multiple_values(instruction_str)
            self.transaction_identifier = values[0].strip()
            self.variable_identifier = values[1].strip()
        elif self.instruction_type == InstructionType.WRITE:
            values = self.get_multiple_values(instruction_str)
            self.transaction_identifier = values[0].strip()
            self.variable_identifier = values[1].strip()
            self.value = values[2].strip()
        elif self.instruction_type == InstructionType.FAIL or \
             self.instruction_type == InstructionType.RECOVER or \
             self.instruction_type == InstructionType.DUMP_SITE:
            self.site_identifier = int(self.get_single_value(instruction_str))
        elif self.instruction_type == InstructionType.DUMP_VAR:
            self.variable_identifier = self.get_single_value(instruction_str)

    def __repr__(self):
        """ Representation of this object """

        return "{ Type: %s, Variable: %s, Site: %s, Transaction: %s, Value: %s}" % \
                (self.instruction_type, self.variable_identifier, str(self.site_identifier), \
                 self.transaction_identifier, self.value)

    def get_type(self, instruction_str):
        """ Gets the type of instruction from the file """
        
        expressions = {
            InstructionType.BEGIN: "begin\(%s\)" % TRANSACTION_EXPR,
            InstructionType.BEGIN_RO: "beginro\(%s\)" % TRANSACTION_EXPR,
            InstructionType.DUMP_ALL: "dump\(\)",
            InstructionType.DUMP_SITE: "dump\(%s\)" % SITE_EXPR,
            InstructionType.DUMP_VAR: "dump\(%s\)" % VARIABLE_EXPR,
            InstructionType.END: "end\(%s\)" % TRANSACTION_EXPR,
            InstructionType.FAIL: "fail\(%s\)" % SITE_EXPR,
            InstructionType.READ: "r\(%s,%s\)" % (TRANSACTION_EXPR, VARIABLE_EXPR),
            InstructionType.RECOVER: "recover\(%s\)" % SITE_EXPR,
            InstructionType.WRITE: "w\(%s,%s,\s*[a-zA-Z0-9]+\s*\)" % (TRANSACTION_EXPR, VARIABLE_EXPR)
        }

        for instruction_type, expr in expressions.iteritems():
            pattern = re.compile(expr, re.IGNORECASE)
            if pattern.match(instruction_str.lower()):
                return instruction_type

    def get_single_value(self, instruction_str):
        """ Returns the value in between parenthesis """

        return instruction_str[instruction_str.find("(")+1:instruction_str.find(")")]

    def get_multiple_values(self, instruction_str):
        """ Returns all values in between parenthesis as an array """

        values = instruction_str[instruction_str.find("(")+1:instruction_str.find(")")]
        return values.split(",")

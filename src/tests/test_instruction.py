# -*- coding: utf-8 -*-
""" Test Instruction Class """
import unittest
from src.objects.instruction import Instruction, InstructionType

class InstructionTestCase(unittest.TestCase):
    """ Test cases for an Instruction """

    def test_begin_instruction_type(self):
        """ Test a Begin Instruction Type """

        instruction = Instruction("begin(T1)")

        self.assertEquals(instruction.instruction_type, InstructionType.BEGIN)
        self.assertEquals(instruction.transaction_identifier, "T1")
        self.assertIsNone(instruction.variable_identifier)
        self.assertIsNone(instruction.site_identifier)
        self.assertIsNone(instruction.value)

    def test_begin_ro_instruction_type(self):
        """ Test a BeginRO Instruction Type """

        instruction = Instruction("beginRO(T1)")

        self.assertEquals(instruction.instruction_type, InstructionType.BEGIN_RO)
        self.assertEquals(instruction.transaction_identifier, "T1")
        self.assertIsNone(instruction.variable_identifier)
        self.assertIsNone(instruction.site_identifier)
        self.assertIsNone(instruction.value)

    def test_dump_all_instruction_type(self):
        """ Test a Dump All Instruction Type """

        instruction = Instruction("dump()")

        self.assertEquals(instruction.instruction_type, InstructionType.DUMP_ALL)
        self.assertIsNone(instruction.transaction_identifier)
        self.assertIsNone(instruction.variable_identifier)
        self.assertIsNone(instruction.site_identifier)
        self.assertIsNone(instruction.value)

    def test_dump_site_instruction_type(self):
        """ Test a Dump Site Instruction Type """

        instruction = Instruction("dump(3)")

        self.assertEquals(instruction.instruction_type, InstructionType.DUMP_SITE)
        self.assertEquals(instruction.site_identifier, 3)
        self.assertIsNone(instruction.transaction_identifier)
        self.assertIsNone(instruction.variable_identifier)
        self.assertIsNone(instruction.value)

    def test_dump_variable_instruction_type(self):
        """ Test a Dump Variable Instruction Type """

        instruction = Instruction("dump(x3)")

        self.assertEquals(instruction.instruction_type, InstructionType.DUMP_VAR)
        self.assertEquals(instruction.variable_identifier, "x3")
        self.assertIsNone(instruction.site_identifier, 3)
        self.assertIsNone(instruction.transaction_identifier)
        self.assertIsNone(instruction.value)

    def test_end_instruction_type(self):
        """ Test a End Instruction Type """

        instruction = Instruction("end(T3)")

        self.assertEquals(instruction.instruction_type, InstructionType.END)
        self.assertEquals(instruction.transaction_identifier, "T3")
        self.assertIsNone(instruction.site_identifier)
        self.assertIsNone(instruction.variable_identifier)
        self.assertIsNone(instruction.value)

    def test_fail_instruction_type(self):
        """ Test a Fail Instruction Type """

        instruction = Instruction("fail(3)")

        self.assertEquals(instruction.instruction_type, InstructionType.FAIL)
        self.assertEquals(instruction.site_identifier, 3)
        self.assertIsNone(instruction.transaction_identifier)
        self.assertIsNone(instruction.variable_identifier)
        self.assertIsNone(instruction.value)

    def test_recover_instruction_type(self):
        """ Test a Recover Instruction Type """

        instruction = Instruction("recover(3)")

        self.assertEquals(instruction.instruction_type, InstructionType.RECOVER)
        self.assertEquals(instruction.site_identifier, 3)
        self.assertIsNone(instruction.transaction_identifier)
        self.assertIsNone(instruction.variable_identifier)
        self.assertIsNone(instruction.value)

    def test_read_instruction_type(self):
        """ Test a Read Instruction Type """

        instruction = Instruction("R(T2,x2)")

        self.assertEquals(instruction.instruction_type, InstructionType.READ)
        self.assertEquals(instruction.transaction_identifier, "T2")
        self.assertEquals(instruction.variable_identifier, "x2")
        self.assertIsNone(instruction.site_identifier)
        self.assertIsNone(instruction.value)

    def test_write_instruction_type(self):
        """ Test a Write Instruction Type """

        instruction = Instruction("W(T1,x3,33)")

        self.assertEquals(instruction.instruction_type, InstructionType.WRITE)
        self.assertEquals(instruction.transaction_identifier, "T1")
        self.assertEquals(instruction.variable_identifier, "x3")
        self.assertEquals(instruction.value, "33")
        self.assertIsNone(instruction.site_identifier)

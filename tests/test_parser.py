# -*- coding: utf-8 -*-
""" Test Parser Class """
import unittest
import os

from src.utilities.parser import Parser
from src.utilities.logger import Logger
from src.objects.instruction import Instruction, InstructionType

class ParserTestCase(unittest.TestCase):
    """ Test cases for Parser """

    @classmethod
    def setUpClass(cls):
        """ Setup Environment """

        # Create a dummy test file
        writer = open('input_test.txt', 'w')
        writer.write("begin(T1)\n")
        writer.write("W(T1,x1,101)\n")
        writer.close()

    @classmethod
    def tearDownClass(cls):
        """ Clean up environment when finished """
        os.remove('input_test.txt')

    def setUp(self):
        self.logger = Logger()
        self.logger.show_stdout()

    def test_valid_input_file(self):
        """ Test that a valid input file can be read """
        parser = Parser('input_test.txt', self.logger)

        instruction = parser.get_instruction()
        self.assertEquals(instruction.instruction_type, InstructionType.BEGIN)
        self.assertEquals(instruction.transaction_identifier, "T1")

        instruction = parser.get_instruction()
        self.assertEquals(instruction.instruction_type, InstructionType.WRITE)
        self.assertEquals(instruction.transaction_identifier, "T1")
        self.assertEquals(instruction.variable_identifier, "x1")
        self.assertEquals(instruction.value, "101")

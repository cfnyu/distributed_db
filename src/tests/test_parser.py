# -*- coding: utf-8 -*-
""" Test Parser Class """
import unittest
import os

from src.utilities.parser import Parser
from src.utilities.logger import Logger

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

        instruction1 = parser.get_instruction()
        self.assertEquals(instruction1.instruction, "begin(T1)")

        instruction2 = parser.get_instruction()
        self.assertEquals(instruction2.instruction, "W(T1,x1,101)")

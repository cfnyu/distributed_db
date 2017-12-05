# -*- coding: utf-8 -*-
""" Test Transaction Manager """
import unittest

from src.objects.clock import Clock
from src.utilities.logger import Logger
from src.transaction_manager import TransactionManager
from src.objects.instruction import Instruction

class TransactionManagerTestCase(unittest.TestCase):
    """ Test cases for the Transaction Manager """

    def setUp(self):
        self.logger = Logger()
        self.logger.show_stdout()
        self.clock = Clock()
        self.clock.tick()

    def test_execute_function_quickly(self):
        """ This method is too broad """
        
        tm = TransactionManager(self.clock.time, self.logger)
        instruction = Instruction("Begin(T1)")
        tm.execute(instruction)

        self.assertEquals(len(tm.sites), 10)

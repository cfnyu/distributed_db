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
        # self.logger.show_stdout()
        self.clock = Clock()
        self.clock.tick()
        self.transaction_manager = TransactionManager(self.clock.time, self.logger)

    def test_execute_begin_transaction(self):
        """ Given a Begin instruction, begin transaction method will be called """
        # TODO: Re-write function once begin_transaction function has been written

        instruction = Instruction("Begin(T1)")
        result = self.transaction_manager.execute(instruction)

        self.assertEquals(result, "Begin Transaction")

    def test_execute_begin_ro_transaction(self):
        """ Given a BeginRO instruction, begin transaction method will be called """
        # TODO: Re-write function once begin_transaction function has been written

        instruction = Instruction("BeginRO(T1)")
        result = self.transaction_manager.execute(instruction)

        self.assertEquals(result, "Begin Transaction")

    def test_execute_dump_all_transaction(self):
        """ Given a Dump All instruction, dump method will be called """
        # TODO: Re-write function once dump function has been written

        instruction = Instruction("dump()")
        result = self.transaction_manager.execute(instruction)

        self.assertEquals(result, "dump")

    def test_execute_dump_site_transaction(self):
        """ Given a Dump Site instruction, dump method will be called """
        # TODO: Re-write function once dump function has been written

        instruction = Instruction("dump(3)")
        result = self.transaction_manager.execute(instruction)

        self.assertEquals(result, "dump")

    def test_execute_dump_var_transaction(self):
        """ Given a Dump Variable instruction, dump method will be called """
        # TODO: Re-write function once dump function has been written

        instruction = Instruction("dump(x9)")
        result = self.transaction_manager.execute(instruction)

        self.assertEquals(result, "dump")

    def test_execute_end_transaction(self):
        """ Given a End instruction, end transaction method will be called """
        # TODO: Re-write function once end function has been written

        instruction = Instruction("end(T1)")
        result = self.transaction_manager.execute(instruction)

        self.assertEquals(result, "Check if a transaction can be committed")

    def test_execute_fail_transaction(self):
        """ Given a Fail instruction, fail method will be called """
        # TODO: Re-write function once fail function has been written

        instruction = Instruction("fail(1)")
        result = self.transaction_manager.execute(instruction)

        self.assertEquals(result, "fail")

    def test_execute_read_transaction(self):
        """ Given a Read instruction, read method will be called """
        # TODO: Re-write function once read function has been written

        instruction = Instruction("R(T2,x2)")
        result = self.transaction_manager.execute(instruction)

        self.assertEquals(result, "Read the value of a Variable")

    def test_execute_recover_transaction(self):
        """ Given a Recover instruction, recover transaction will be called """
        # TODO: Re-write function once recover function has been written

        instruction = Instruction("recover(1)")
        result = self.transaction_manager.execute(instruction)

        self.assertEquals(result, "recover")

    def test_execute_write_transaction(self):
        """ Given a Write instruction, write transaction will be called """
        # TODO: Re-write function once write function has been written

        instruction = Instruction("W(T1,x3,33)")
        result = self.transaction_manager.execute(instruction)

        self.assertEquals(result, "Write the value of a Variable")

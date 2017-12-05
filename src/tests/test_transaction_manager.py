# -*- coding: utf-8 -*-
""" Test Transaction Manager """
import unittest
import sys
from contextlib import contextmanager
from StringIO import StringIO
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

        instruction = Instruction("dump()")

        with captured_output() as (out, err):
            self.transaction_manager.execute(instruction)

        output = out.getvalue().strip()
        self.assertEqual(output, "{1: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 2: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x11': { x11: 110 }, 'x12': { x12: 120 }, 'x1': { x1: 10 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 3: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 4: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x3': { x3: 30 }, 'x12': { x12: 120 }, 'x13': { x13: 130 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 5: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 6: {'x14': { x14: 140 }, 'x20': { x20: 200 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x15': { x15: 150 }, 'x4': { x4: 40 }, 'x5': { x5: 50 }}, 7: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 8: {'x14': { x14: 140 }, 'x20': { x20: 200 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x7': { x7: 70 }, 'x4': { x4: 40 }, 'x17': { x17: 170 }}, 9: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 10: {'x19': { x19: 190 }, 'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x9': { x9: 90 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}}")

    def test_execute_dump_site_transaction(self):
        """ Given a Dump Site instruction, dump method will be called """

        instruction = Instruction("dump(3)")

        with captured_output() as (out, err):
            self.transaction_manager.execute(instruction)

        output = out.getvalue().strip()
        self.assertEqual(output, "{'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}")


    def test_execute_dump_var_transaction(self):
        """ Given a Dump Variable instruction, dump method will be called """

        instruction = Instruction("dump(3)")

        with captured_output() as (out, err):
            self.transaction_manager.execute(instruction)

        output = out.getvalue().strip()
        self.assertEqual(output, "{'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}")

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

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

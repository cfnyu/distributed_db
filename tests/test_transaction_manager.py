# -*- coding: utf-8 -*-
""" Test Transaction Manager """
import unittest
import sys
from contextlib import contextmanager
from StringIO import StringIO
from src.objects.transaction import TransactionType, TransactionState
from src.objects.instruction import Instruction
from src.transaction_manager import TransactionManager
from src.utilities.logger import Logger

class TransactionManagerTestCase(unittest.TestCase):
    """ Test cases for the Transaction Manager """

    def setUp(self):
        self.logger = Logger()
        # self.logger.show_stdout()
        self.transaction_manager = TransactionManager(self.logger)

    def test_constructor(self):
        """ Test that the constructor is doing what is expected """
        pass

    def test_execute_begin_transaction_read_write(self):
        """ Testing a Read/Write Begin transaction statement """

        instruction = Instruction("Begin(T1)")
        self.transaction_manager.execute(instruction)
        trans1 = self.transaction_manager.transactions["T1"]
        self.assertEquals(len(self.transaction_manager.transactions), 1)
        self.assertEquals(trans1.identifier, "T1")
        self.assertEquals(trans1.transaction_type, TransactionType.READ_WRITE)
        self.assertEquals(trans1.start_time, 1)
        self.assertIsNone(trans1.end_time)
        self.assertEquals(trans1.state, TransactionState.RUNNING)

    def test_execute_begin_ro_transaction(self):
        """ Testing a Read Only Begin transaction statement """

        instruction = Instruction("BeginRO(T1)")
        self.transaction_manager.execute(instruction)
        trans1 = self.transaction_manager.transactions["T1"]

        self.assertTrue("T1" in self.transaction_manager.transactions)
        self.assertEquals(self.transaction_manager.transactions["T1"].transaction_type, TransactionType.READ_ONLY)

        print self.transaction_manager.readonly_snapshots
        for site in self.transaction_manager.sites.values():
            for variable_identifier in site.data_manager.variables:
                self.assertTrue(variable_identifier in self.transaction_manager.readonly_snapshots["T1"])
                
        self.assertEquals(trans1.identifier, "T1")
        self.assertEquals(trans1.transaction_type, TransactionType.READ_ONLY)
        self.assertEquals(trans1.start_time, 1)
        self.assertIsNone(trans1.end_time)
        self.assertEquals(trans1.state, TransactionState.RUNNING)

    def test_begin_ro_transaction_snapshot(self):
        """ Testing that a snapshot holds the correct values """

        instruction = Instruction("BeginRO(T1)")
        self.transaction_manager.execute(instruction)
        for site in self.transaction_manager.sites.values():
            self.assertTrue(len(site.data_manager.variables) > 0)
            for variable_identifier in site.data_manager.variables:
                self.assertTrue(variable_identifier in self.transaction_manager.readonly_snapshots["T1"])

    @unittest.skip("Unrealistic output to test")
    def test_execute_dump_all_transaction(self):
        """ Given a Dump All instruction, dump method will be called """

        instruction = Instruction("dump()")

        with std_out() as (out, err):
            self.transaction_manager.execute(instruction)

        output = out.getvalue().strip()

        self.assertEqual(output, "{1: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 2: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x11': { x11: 110 }, 'x12': { x12: 120 }, 'x1': { x1: 10 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 3: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 4: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x3': { x3: 30 }, 'x12': { x12: 120 }, 'x13': { x13: 130 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 5: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 6: {'x14': { x14: 140 }, 'x20': { x20: 200 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x15': { x15: 150 }, 'x4': { x4: 40 }, 'x5': { x5: 50 }}, 7: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 8: {'x14': { x14: 140 }, 'x20': { x20: 200 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x7': { x7: 70 }, 'x4': { x4: 40 }, 'x17': { x17: 170 }}, 9: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 10: {'x19': { x19: 190 }, 'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x9': { x9: 90 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}}")

    @unittest.skip("Unrealistic output to test")
    def test_execute_dump_site_transaction(self):
        """ Given a Dump Site instruction, dump method will be called """

        instruction = Instruction("dump(3)")

        with std_out() as (out, err):
            self.transaction_manager.execute(instruction)

        output = out.getvalue().strip()
        self.assertEqual(output, "{'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}")

    @unittest.skip("Unrealistic output to test")
    def test_execute_dump_var_transaction(self):
        """ Given a Dump Variable instruction, dump method will be called """

        instruction = Instruction("dump(3)")

        with std_out() as (out, err):
            self.transaction_manager.execute(instruction)

        output = out.getvalue().strip()
        self.assertEqual(output, "{'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}")

@contextmanager
def std_out():
    """ Capture stdout """

    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

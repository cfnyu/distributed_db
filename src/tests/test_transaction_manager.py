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
        self.assertEquals(trans1.state, TransactionState.WAITING)

    def test_execute_begin_ro_transaction(self):
        """ Testing a Read Only Begin transaction statement """

        instruction = Instruction("BeginRO(T1)")
        self.transaction_manager.execute(instruction)
        trans1 = self.transaction_manager.transactions["T1"]

        self.assertEquals(len(self.transaction_manager.transactions), 1)
        self.assertTrue(instruction.transaction_identifier in self.transaction_manager.readonly_snapshots)
        self.assertEquals(len(self.transaction_manager.readonly_snapshots["T1"].keys()), 10)
        self.assertEquals(trans1.identifier, "T1")
        self.assertEquals(trans1.transaction_type, TransactionType.READ_ONLY)
        self.assertEquals(trans1.start_time, 1)
        self.assertIsNone(trans1.end_time)
        self.assertEquals(trans1.state, TransactionState.WAITING)

    def test_begin_ro_transaction_snapshot(self):
        """ Testing that a snapshot holds the correct values """

        instruction = Instruction("BeginRO(T1)")
        self.transaction_manager.execute(instruction)
        trans1 = self.transaction_manager.readonly_snapshots["T1"]
        site_1 = trans1[1]
        site_2 = trans1[2]
        site_3 = trans1[3]
        site_3 = trans1[3]
        site_4 = trans1[4]
        site_5 = trans1[5]
        site_6 = trans1[6]
        site_7 = trans1[7]
        site_8 = trans1[8]
        site_9 = trans1[9]
        site_10 = trans1[10]

        self.assertTrue(instruction.transaction_identifier in self.transaction_manager.readonly_snapshots)
        self.assertEquals(len(trans1.keys()), 10)
        self.assertEquals(site_1, ['x14', 'x18', 'x10', 'x8', 'x16', 'x2', 'x12', 'x6', 'x20', 'x4'])
        self.assertEquals(site_2, ['x14', 'x18', 'x10', 'x8', 'x16', 'x2', 'x11', 'x12', 'x1', 'x6', 'x20', 'x4'])
        self.assertEquals(site_3, ['x14', 'x18', 'x10', 'x8', 'x16', 'x2', 'x12', 'x6', 'x20', 'x4'])
        self.assertEquals(site_4, ['x14', 'x18', 'x10', 'x8', 'x16', 'x2', 'x3', 'x12', 'x13', 'x6', 'x20', 'x4'])
        self.assertEquals(site_5, ['x14', 'x18', 'x10', 'x8', 'x16', 'x2', 'x12', 'x6', 'x20', 'x4'])
        self.assertEquals(site_6, ['x14', 'x20', 'x18', 'x10', 'x8', 'x16', 'x2', 'x12', 'x6', 'x15', 'x4', 'x5'])
        self.assertEquals(site_7, ['x14', 'x18', 'x10', 'x8', 'x16', 'x2', 'x12', 'x6', 'x20', 'x4'])
        self.assertEquals(site_8, ['x14', 'x20', 'x18', 'x10', 'x8', 'x16', 'x2', 'x12', 'x6', 'x7', 'x4', 'x17'])
        self.assertEquals(site_9, ['x14', 'x18', 'x10', 'x8', 'x16', 'x2', 'x12', 'x6', 'x20', 'x4'])
        self.assertEquals(site_10, ['x19', 'x14', 'x18', 'x10', 'x8', 'x9', 'x16', 'x2', 'x12', 'x6', 'x20', 'x4'])

    def test_execute_dump_all_transaction(self):
        """ Given a Dump All instruction, dump method will be called """

        instruction = Instruction("dump()")

        with std_out() as (out, err):
            self.transaction_manager.execute(instruction)

        output = out.getvalue().strip()

        self.assertEqual(output, "{1: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 2: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x11': { x11: 110 }, 'x12': { x12: 120 }, 'x1': { x1: 10 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 3: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 4: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x3': { x3: 30 }, 'x12': { x12: 120 }, 'x13': { x13: 130 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 5: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 6: {'x14': { x14: 140 }, 'x20': { x20: 200 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x15': { x15: 150 }, 'x4': { x4: 40 }, 'x5': { x5: 50 }}, 7: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 8: {'x14': { x14: 140 }, 'x20': { x20: 200 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x7': { x7: 70 }, 'x4': { x4: 40 }, 'x17': { x17: 170 }}, 9: {'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}, 10: {'x19': { x19: 190 }, 'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x9': { x9: 90 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}}")

    def test_execute_dump_site_transaction(self):
        """ Given a Dump Site instruction, dump method will be called """

        instruction = Instruction("dump(3)")

        with std_out() as (out, err):
            self.transaction_manager.execute(instruction)

        output = out.getvalue().strip()
        self.assertEqual(output, "{'x14': { x14: 140 }, 'x18': { x18: 180 }, 'x10': { x10: 100 }, 'x8': { x8: 80 }, 'x16': { x16: 160 }, 'x2': { x2: 20 }, 'x12': { x12: 120 }, 'x6': { x6: 60 }, 'x20': { x20: 200 }, 'x4': { x4: 40 }}")


    def test_execute_dump_var_transaction(self):
        """ Given a Dump Variable instruction, dump method will be called """

        instruction = Instruction("dump(3)")

        with std_out() as (out, err):
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

    def test_execute_recover_transaction(self):
        """ Given a Recover instruction, recover transaction will be called """
        # TODO: Re-write function once recover function has been written

        instruction = Instruction("recover(1)")
        result = self.transaction_manager.execute(instruction)

        self.assertEquals(result, "recover")

    def test_execute_write_transaction(self):
        """ Given a Write instruction, write transaction will be called """
        
        instruction = Instruction("W(T1,x3,33)")
        self.assertRaises(ValueError, self.transaction_manager.execute, instruction)

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


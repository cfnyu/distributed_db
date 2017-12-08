# -*- coding: utf-8 -*-
""" Test Input File Two """
import unittest
import sys
import os 
from contextlib import contextmanager
from StringIO import StringIO
from src.objects.instruction import Instruction, InstructionType
from src.objects.lock import Lock, LockType
from src.objects.site import SiteStatus
from src.objects.transaction import Transaction, TransactionType, TransactionState
from src.objects.variable import Variable
from src.sites.data_manager import DataManager
from src.transaction_manager import TransactionManager
from src.utilities.logger import Logger
from src.utilities.parser import Parser

DEFAULT_START_TIME = 0

class InputTwoTestCase(unittest.TestCase):
    """ Test cases for Input File Two """

    def setUp(self):
        self.logger = Logger()
        self.transaction_manager = TransactionManager(self.logger)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.input_dir = dir_path.replace("/tests/input_files", "/samples")

    def tearDown(self):
        self.transaction_manager = None

    def test_input_2(self):
        """ Test the second input file """

        parser = Parser(self.input_dir + "/input_2", self.logger)

        begin_t1 = parser.get_instruction()
        self.assertEquals(begin_t1.instruction_type, InstructionType.BEGIN)
        self.assertEquals(begin_t1.transaction_identifier, "T1")

        self.transaction_manager.execute(begin_t1)
        self.assertTrue(begin_t1.transaction_identifier in self.transaction_manager.transactions)

        begin_ro_t2 = parser.get_instruction()
        self.assertEquals(begin_ro_t2.instruction_type, InstructionType.BEGIN_RO)
        self.assertEquals(begin_ro_t2.transaction_identifier, "T2")

        self.transaction_manager.execute(begin_ro_t2)
        self.assertTrue(begin_ro_t2.transaction_identifier in self.transaction_manager.transactions)
        self.assertTrue("T2" in self.transaction_manager.readonly_snapshots)

        for site in self.transaction_manager.sites.values():
            for variable_identifier, variable in site.data_manager.variables.iteritems():
                self.assertTrue(variable_identifier in self.transaction_manager.readonly_snapshots["T2"])
                self.assertEquals(self.transaction_manager.readonly_snapshots["T2"][variable_identifier], variable.value)

        write_t1_x1 = parser.get_instruction()
        self.assertEquals(write_t1_x1.instruction_type, InstructionType.WRITE)
        self.assertEquals(write_t1_x1.transaction_identifier, "T1")
        self.assertEquals(write_t1_x1.variable_identifier, "x1")
        self.assertEquals(write_t1_x1.value, "101")

        self.transaction_manager.execute(write_t1_x1)
        self.assertEquals(self.transaction_manager.transactions["T1"].state, \
                          TransactionState.RUNNING)

        for site_id, site in self.transaction_manager.sites.iteritems():
            self.assertEquals(site.status, SiteStatus.UP)
            if site_id == 2:
                self.assertTrue("x1" in site.data_manager.variables)
                variable = site.data_manager.variables["x1"]
                self.assertEquals(variable.index, 1)
                self.assertEquals(variable.identifier, "x1")
                self.assertEquals(variable.replicated, False)
                self.assertEquals(variable.readable, True)
                self.assertEquals(variable.value, "10")
                self.assertEquals(variable.written_values[DEFAULT_START_TIME], "10")
                self.assertTrue(len(variable.written_values) == 1)

                self.assertTrue("x1" in site.data_manager.locks)
                self.assertTrue("T1" in site.data_manager.entries)
                self.assertTrue("x1" in site.data_manager.entries["T1"])
                self.assertEquals(site.data_manager.entries["T1"]["x1"].written_values[DEFAULT_START_TIME], "10")
                self.assertTrue("T1" in self.transaction_manager.sites_transactions_read_write_log)
            else:
                self.assertFalse("x1" in site.data_manager.variables)
                self.assertFalse("x1" in site.data_manager.locks)

        self.assertEquals(self.transaction_manager.sites_transactions_read_write_log["T1"], set([2]))
        self.assertTrue("T1" in self.transaction_manager.sites_transactions_accessed_log)
        self.assertEquals(self.transaction_manager.sites_transactions_accessed_log["T1"], \
                        set([self.transaction_manager.sites[2]]))

        read_t2_x2 = parser.get_instruction()
        self.assertEquals(read_t2_x2.instruction_type, InstructionType.READ)
        self.assertEquals(read_t2_x2.transaction_identifier, "T2")
        self.assertEquals(read_t2_x2.variable_identifier, "x2")

        with std_out() as (out, err):
            self.transaction_manager.execute(read_t2_x2)

        output = out.getvalue().strip()
        self.assertEquals(output, "T2: Read x2 - value 20")

        self.assertFalse("T2" in self.transaction_manager.sites_transactions_read_write_log)
        self.assertFalse("T2" in self.transaction_manager.sites_transactions_accessed_log)

        write_t1_x2 = parser.get_instruction()
        self.assertEquals(write_t1_x2.instruction_type, InstructionType.WRITE)
        self.assertEquals(write_t1_x2.transaction_identifier, "T1")
        self.assertEquals(write_t1_x2.variable_identifier, "x2")
        self.assertEquals(write_t1_x2.value, "102")

        self.transaction_manager.execute(write_t1_x2)
        self.assertEquals(self.transaction_manager.transactions["T2"].state, \
                          TransactionState.RUNNING)

        for site_id, site in self.transaction_manager.sites.iteritems():
            self.assertEquals(site.status, SiteStatus.UP)

            self.assertTrue("x2" in site.data_manager.variables)
            variable = site.data_manager.variables["x2"]
            self.assertEquals(variable.index, 2)
            self.assertEquals(variable.identifier, "x2")
            self.assertEquals(variable.replicated, True)
            self.assertEquals(variable.readable, True)
            self.assertEquals(variable.value, "20")
            self.assertEquals(variable.written_values[DEFAULT_START_TIME], "20")
            self.assertTrue(len(variable.written_values) == 1)

            self.assertTrue("x2" in site.data_manager.locks)
            self.assertTrue("T1" in site.data_manager.entries)
            self.assertTrue("x2" in site.data_manager.entries["T1"])
            self.assertEquals(site.data_manager.entries["T1"]["x2"].written_values[DEFAULT_START_TIME], "20")

        self.assertTrue("T1" in self.transaction_manager.sites_transactions_read_write_log)
        self.assertEquals(self.transaction_manager.sites_transactions_read_write_log["T1"], \
                          set(self.transaction_manager.sites.keys()))

        self.assertTrue("T1" in self.transaction_manager.sites_transactions_accessed_log)
        self.assertEquals(self.transaction_manager.sites_transactions_accessed_log["T1"], \
                            set(self.transaction_manager.sites.values()))

        read_t2_x1 = parser.get_instruction()
        self.assertEquals(read_t2_x1.instruction_type, InstructionType.READ)
        self.assertEquals(read_t2_x1.transaction_identifier, "T2")
        self.assertEquals(read_t2_x1.variable_identifier, "x1")

        with std_out() as (out, err):
            self.transaction_manager.execute(read_t2_x1)

        output = out.getvalue().strip()
        self.assertEquals(output, "T2: Read x1 - value 10")
        self.assertFalse("T2" in self.transaction_manager.sites_transactions_read_write_log)
        self.assertFalse("T2" in self.transaction_manager.sites_transactions_accessed_log)

        end_t1 = parser.get_instruction()
        self.assertEquals(end_t1.instruction_type, InstructionType.END)
        self.assertEquals(end_t1.transaction_identifier, "T1")

        with std_out() as (out, err):
            self.transaction_manager.execute(end_t1)

        output = out.getvalue().strip()
        self.assertEquals(output, "T1 committed")

        self.assertEquals(self.transaction_manager.transactions["T1"].state, TransactionState.COMMITTED)
        self.assertEquals(self.transaction_manager.transactions["T1"].transaction_type, TransactionType.READ_WRITE)

        end_t2 = parser.get_instruction()
        self.assertEquals(end_t2.instruction_type, InstructionType.END)
        self.assertEquals(end_t2.transaction_identifier, "T2")

        with std_out() as (out, err):
            self.transaction_manager.execute(end_t2)

        output = out.getvalue().strip()
        self.assertEquals(output, "T2 committed")

        self.assertEquals(self.transaction_manager.transactions["T2"].state, TransactionState.COMMITTED)
        self.assertEquals(self.transaction_manager.transactions["T2"].transaction_type, TransactionType.READ_ONLY)

        self.assertTrue(len(self.transaction_manager.sites_transactions_accessed_log) == 0)
        self.assertTrue(len(self.transaction_manager.waiting_transactions_instructions_map) == 0)
        self.assertTrue(len(self.transaction_manager.blocked_transactions_instructions_map) == 0)
        self.assertTrue(len(self.transaction_manager.sites_transactions_read_write_log) == 0)

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


# -*- coding: utf-8 -*-
""" Test Input File Five """
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

class InputFiveTestCase(unittest.TestCase):
    """ Test cases for Input File Five """

    def setUp(self):
        self.logger = Logger()
        self.transaction_manager = TransactionManager(self.logger)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.input_dir = dir_path.replace("/tests/input_files", "/samples")

    def tearDown(self):
        self.transaction_manager = None

    def test_input_5(self):
        """ Test the Five input file """

        parser = Parser(self.input_dir + "/input_5", self.logger)

        begin_t1 = parser.get_instruction()
        self.assertEquals(begin_t1.instruction_type, InstructionType.BEGIN)
        self.assertEquals(begin_t1.transaction_identifier, "T1")

        self.transaction_manager.execute(begin_t1)
        self.assertTrue(begin_t1.transaction_identifier in self.transaction_manager.transactions)

        begin_t2 = parser.get_instruction()
        self.assertEquals(begin_t2.instruction_type, InstructionType.BEGIN)
        self.assertEquals(begin_t2.transaction_identifier, "T2")

        self.transaction_manager.execute(begin_t2)
        self.assertTrue(begin_t2.transaction_identifier in self.transaction_manager.transactions)

        write_t1_x6 = parser.get_instruction()
        self.assertEquals(write_t1_x6.instruction_type, InstructionType.WRITE)
        self.assertEquals(write_t1_x6.transaction_identifier, "T1")
        self.assertEquals(write_t1_x6.variable_identifier, "x6")
        self.assertEquals(write_t1_x6.value, "66")
        self.transaction_manager.execute(write_t1_x6)

        self.assertEquals(self.transaction_manager.transactions["T1"].state, \
                          TransactionState.RUNNING)
        accessed_sites = set()
        accessed_site_ids = set([1, 3, 4, 5, 6, 7, 8, 9, 10])

        for site_id, site in self.transaction_manager.sites.iteritems():
            self.assertTrue("x6" in site.data_manager.variables)
            self.assertEquals(site.status, SiteStatus.UP)

            variable = site.data_manager.variables["x6"]
            self.assertEquals(variable.index, 6)
            self.assertEquals(variable.identifier, "x6")
            self.assertEquals(variable.replicated, True)
            self.assertEquals(variable.readable, True)
            self.assertEquals(variable.value, "60")
            self.assertEquals(variable.written_values[DEFAULT_START_TIME], "60")
            self.assertTrue(len(variable.written_values) == 1)

            self.assertTrue("x6" in site.data_manager.locks)
            self.assertTrue("T1" in site.data_manager.entries)
            self.assertTrue("x6" in site.data_manager.entries["T1"])
            self.assertTrue(len(site.data_manager.entries["T1"]["x6"].written_values) == 2)

            self.assertEquals(site.data_manager.entries["T1"]["x6"] \
                                .written_values[DEFAULT_START_TIME], "60")

            self.assertEquals(site.data_manager.entries["T1"]["x6"] \
                                .written_values[DEFAULT_START_TIME + 3], "66") # 3rd Instruction
            accessed_sites.add(site)

        self.assertEquals(self.transaction_manager.sites_transactions_read_write_log["T1"], \
                            set(self.transaction_manager.sites.keys()))

        self.assertTrue("T1" in self.transaction_manager.sites_transactions_accessed_log)
        self.assertEquals(self.transaction_manager.sites_transactions_accessed_log["T1"], \
                            set(self.transaction_manager.sites.values()))

        fail_2 = parser.get_instruction()
        self.assertEquals(fail_2.instruction_type, InstructionType.FAIL)
        self.assertEquals(fail_2.site_identifier, 2)
        self.assertIsNone(fail_2.transaction_identifier)
        self.assertIsNone(fail_2.variable_identifier)
        self.assertIsNone(fail_2.value)

        with std_out() as (out, err):
            self.transaction_manager.execute(fail_2)

        output = out.getvalue().strip()
        self.assertEquals(output, "T1 was aborted because it performed read or write operation on failed site 2.")

        self.assertEquals(self.transaction_manager.sites[2].status, SiteStatus.DOWN)
        self.assertTrue(len(self.transaction_manager.sites[2].data_manager.locks) == 0)
        self.assertTrue(len(self.transaction_manager.sites[2].data_manager.entries) == 0)

        write_t2_x8 = parser.get_instruction()
        self.assertEquals(write_t2_x8.instruction_type, InstructionType.WRITE)
        self.assertEquals(write_t2_x8.transaction_identifier, "T2")
        self.assertEquals(write_t2_x8.variable_identifier, "x8")
        self.assertEquals(write_t2_x8.value, "88")
        self.transaction_manager.execute(write_t2_x8)

        self.assertEquals(self.transaction_manager.transactions["T2"].state, \
                          TransactionState.RUNNING)
        accessed_sites = set()
        accessed_site_ids = set([1, 3, 4, 5, 6, 7, 8, 9, 10])

        for site_id, site in self.transaction_manager.sites.iteritems():
            self.assertTrue("x8" in site.data_manager.variables)

            if site_id == 2:
                self.assertEquals(site.status, SiteStatus.DOWN)
            else:
                self.assertEquals(site.status, SiteStatus.UP)

            if site_id == 2:
                variable = site.data_manager.variables["x8"]
                self.assertEquals(variable.index, 8)
                self.assertEquals(variable.identifier, "x8")
                self.assertEquals(variable.replicated, True)
                self.assertEquals(variable.readable, True)
                self.assertEquals(variable.value, "80")
                self.assertEquals(variable.written_values[DEFAULT_START_TIME], "80")
                self.assertTrue(len(variable.written_values) == 1)

                self.assertFalse("x8" in site.data_manager.locks)
                self.assertFalse("T2" in site.data_manager.entries)
            else:
                variable = site.data_manager.variables["x8"]
                self.assertEquals(variable.index, 8)
                self.assertEquals(variable.identifier, "x8")
                self.assertEquals(variable.replicated, True)
                self.assertEquals(variable.readable, True)
                self.assertEquals(variable.value, "80")
                self.assertEquals(variable.written_values[DEFAULT_START_TIME], "80")
                self.assertTrue(len(variable.written_values) == 1)

                self.assertTrue("x8" in site.data_manager.locks)
                self.assertTrue("T2" in site.data_manager.entries)
                self.assertTrue("x8" in site.data_manager.entries["T2"])
                self.assertTrue(len(site.data_manager.entries["T2"]["x8"].written_values) == 2)

                self.assertEquals(site.data_manager.entries["T2"]["x8"] \
                                    .written_values[DEFAULT_START_TIME], "80")

                self.assertEquals(site.data_manager.entries["T2"]["x8"] \
                                    .written_values[DEFAULT_START_TIME + 5], "88") # 5th Instruction
                accessed_sites.add(site)

        self.assertEquals(self.transaction_manager.sites_transactions_read_write_log["T2"], \
                            accessed_site_ids)

        self.assertTrue("T2" in self.transaction_manager.sites_transactions_accessed_log)
        self.assertEquals(self.transaction_manager.sites_transactions_accessed_log["T2"], \
                            accessed_sites)

        read_t2_x3 = parser.get_instruction()
        self.assertEquals(read_t2_x3.instruction_type, InstructionType.READ)
        self.assertEquals(read_t2_x3.transaction_identifier, "T2")
        self.assertEquals(read_t2_x3.variable_identifier, "x3")

        with std_out() as (out, err):
            self.transaction_manager.execute(read_t2_x3)

        output = out.getvalue().strip()
        self.assertEquals(output, "T2: Read x3 - value 30 at site 4")

        self.assertTrue("T2" in self.transaction_manager.sites_transactions_read_write_log)
        self.assertEquals(self.transaction_manager.sites_transactions_read_write_log["T2"], \
                          accessed_site_ids)

        self.assertTrue("T2" in self.transaction_manager.sites_transactions_accessed_log)
        self.assertEquals(self.transaction_manager.sites_transactions_accessed_log["T2"], \
                          accessed_sites) # Un-replicated variable

        read_t1_x5 = parser.get_instruction()
        self.assertEquals(read_t1_x5.instruction_type, InstructionType.READ)
        self.assertEquals(read_t1_x5.transaction_identifier, "T1")
        self.assertEquals(read_t1_x5.variable_identifier, "x5")
        self.assertEquals(self.transaction_manager.transactions["T1"].state, \
                          TransactionState.ABORTED)

        with std_out() as (out, err):
            self.transaction_manager.execute(read_t1_x5)

        output = out.getvalue().strip()
        self.assertEquals(output, "") # No print statement for aborted transactions

        self.assertFalse("T1" in self.transaction_manager.sites_transactions_read_write_log)
        self.assertFalse("T1" in self.transaction_manager.sites_transactions_accessed_log)

        end_t2 = parser.get_instruction()
        self.assertEquals(end_t2.instruction_type, InstructionType.END)
        self.assertEquals(end_t2.transaction_identifier, "T2")

        with std_out() as (out, err):
            self.transaction_manager.execute(end_t2)

        output = out.getvalue().strip()
        self.assertEquals(output, "T2 committed")

        self.assertEquals(self.transaction_manager.transactions["T2"].state, \
                            TransactionState.COMMITTED)

        self.assertFalse("T2" in self.transaction_manager.sites_transactions_accessed_log)
        self.assertFalse("T2" in self.transaction_manager.sites_transactions_read_write_log)
        self.assertEquals(self.transaction_manager.transactions["T2"].state, TransactionState.COMMITTED)

        recover_2 = parser.get_instruction()
        self.assertEquals(recover_2.instruction_type, InstructionType.RECOVER)
        self.assertEquals(recover_2.site_identifier, 2)
        self.assertIsNone(recover_2.transaction_identifier)
        self.assertIsNone(recover_2.variable_identifier)
        self.assertIsNone(recover_2.value)
        self.transaction_manager.execute(recover_2)

        self.assertEquals(self.transaction_manager.sites[2].status, SiteStatus.UP)
        for variable in self.transaction_manager.sites[2].data_manager.variables.values():
            if variable.replicated:
                self.assertFalse(variable.readable)
            else:
                self.assertTrue(variable.readable)

        end_t1 = parser.get_instruction()
        self.assertEquals(end_t1.instruction_type, InstructionType.END)
        self.assertEquals(end_t1.transaction_identifier, "T1")

        with std_out() as (out, err):
            self.transaction_manager.execute(end_t1)

        output = out.getvalue().strip()
        self.assertEquals(output, "") # Already aborted
        self.assertEquals(self.transaction_manager.transactions["T1"].state, TransactionState.ABORTED)

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


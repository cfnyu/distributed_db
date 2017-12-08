# -*- coding: utf-8 -*-
""" Test Input File Twenty """
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

class InputTwentyTestCase(unittest.TestCase):
    """ Test cases for Input File Twenty """

    def setUp(self):
        self.logger = Logger()
        self.transaction_manager = TransactionManager(self.logger)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.input_dir = dir_path.replace("/tests/input_files", "/samples")

    def tearDown(self):
        self.transaction_manager = None

    def test_input_20(self):
        """ Test the twentieth input file """

        parser = Parser(self.input_dir + "/input_20", self.logger)

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

        write_t1_x2 = parser.get_instruction()
        self.assertEquals(write_t1_x2.instruction_type, InstructionType.WRITE)
        self.assertEquals(write_t1_x2.transaction_identifier, "T1")
        self.assertEquals(write_t1_x2.variable_identifier, "x2")
        self.assertEquals(write_t1_x2.value, "22")

        self.transaction_manager.execute(write_t1_x2)
        self.assertEquals(self.transaction_manager.transactions["T1"].state, \
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
            self.assertEquals(site.data_manager.entries["T1"]["x2"].written_values[DEFAULT_START_TIME], "20")
            self.assertEquals(site.data_manager.entries["T1"]["x2"].written_values[3], "22")

        self.assertEquals(self.transaction_manager.sites_transactions_read_write_log["T1"], \
                        set(self.transaction_manager.sites.keys()))
        self.assertTrue("T1" in self.transaction_manager.sites_transactions_accessed_log)
        self.assertEquals(self.transaction_manager.sites_transactions_accessed_log["T1"], \
                        set(self.transaction_manager.sites.values()))

        write_t2_x4 = parser.get_instruction()
        self.assertEquals(write_t2_x4.instruction_type, InstructionType.WRITE)
        self.assertEquals(write_t2_x4.transaction_identifier, "T2")
        self.assertEquals(write_t2_x4.variable_identifier, "x4")
        self.assertEquals(write_t2_x4.value, "44")

        self.transaction_manager.execute(write_t2_x4)
        self.assertEquals(self.transaction_manager.transactions["T2"].state, \
                          TransactionState.RUNNING)

        for site_id, site in self.transaction_manager.sites.iteritems():
            self.assertEquals(site.status, SiteStatus.UP)

            self.assertTrue("x4" in site.data_manager.variables)
            variable = site.data_manager.variables["x4"]
            self.assertEquals(variable.index, 4)
            self.assertEquals(variable.identifier, "x4")
            self.assertEquals(variable.replicated, True)
            self.assertEquals(variable.readable, True)
            self.assertEquals(variable.value, "40")
            self.assertEquals(variable.written_values[DEFAULT_START_TIME], "40")
            self.assertTrue(len(variable.written_values) == 1)

            self.assertTrue("x4" in site.data_manager.locks)
            self.assertTrue("T2" in site.data_manager.entries)
            self.assertTrue("x4" in site.data_manager.entries["T2"])
            self.assertEquals(site.data_manager.entries["T2"]["x4"].written_values[DEFAULT_START_TIME], "40")

        self.assertTrue("T2" in self.transaction_manager.sites_transactions_read_write_log)
        self.assertEquals(self.transaction_manager.sites_transactions_read_write_log["T2"], \
                          set(self.transaction_manager.sites.keys()))

        self.assertTrue("T2" in self.transaction_manager.sites_transactions_accessed_log)
        self.assertEquals(self.transaction_manager.sites_transactions_accessed_log["T2"], \
                            set(self.transaction_manager.sites.values()))

        read_t1_x2 = parser.get_instruction()
        self.assertEquals(read_t1_x2.instruction_type, InstructionType.READ)
        self.assertEquals(read_t1_x2.transaction_identifier, "T1")
        self.assertEquals(read_t1_x2.variable_identifier, "x2")

        with std_out() as (out, err):
            self.transaction_manager.execute(read_t1_x2)

        output = out.getvalue().strip()
        self.assertEquals(output, "T1: Read x2 - value 22 at site 1")

        self.assertTrue("T1" in self.transaction_manager.sites_transactions_read_write_log)
        self.assertEquals(self.transaction_manager.sites_transactions_read_write_log["T1"], \
                          set(self.transaction_manager.sites.keys()))

        self.assertTrue("T2" in self.transaction_manager.sites_transactions_accessed_log)
        self.assertEquals(self.transaction_manager.sites_transactions_accessed_log["T2"], \
                          set(self.transaction_manager.sites.values()))

        write_t1_x2 = parser.get_instruction()
        self.assertEquals(write_t1_x2.instruction_type, InstructionType.WRITE)
        self.assertEquals(write_t1_x2.transaction_identifier, "T1")
        self.assertEquals(write_t1_x2.variable_identifier, "x2")
        self.assertEquals(write_t1_x2.value, "98")

        self.transaction_manager.execute(write_t1_x2)
        self.assertEquals(self.transaction_manager.transactions["T1"].state, \
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
            self.assertEquals(site.data_manager.entries["T1"]["x2"].written_values[3], "22")
            self.assertEquals(site.data_manager.entries["T1"]["x2"].written_values[6], "98")

        self.assertTrue("T1" in self.transaction_manager.sites_transactions_read_write_log)
        self.assertEquals(self.transaction_manager.sites_transactions_read_write_log["T1"], \
                          set(self.transaction_manager.sites.keys()))

        self.assertTrue("T1" in self.transaction_manager.sites_transactions_accessed_log)
        self.assertEquals(self.transaction_manager.sites_transactions_accessed_log["T1"], \
                            set(self.transaction_manager.sites.values()))

        end_t2 = parser.get_instruction()
        self.assertEquals(end_t2.instruction_type, InstructionType.END)
        self.assertEquals(end_t2.transaction_identifier, "T2")

        with std_out() as (out, err):
            self.transaction_manager.execute(end_t2)

        output = out.getvalue().strip()
        self.assertEquals(output, "T2 committed")

        read_t1_x2 = parser.get_instruction()
        self.assertEquals(read_t1_x2.instruction_type, InstructionType.READ)
        self.assertEquals(read_t1_x2.transaction_identifier, "T1")
        self.assertEquals(read_t1_x2.variable_identifier, "x2")

        with std_out() as (out, err):
            self.transaction_manager.execute(read_t1_x2)

        output = out.getvalue().strip()
        self.assertEquals(output, "T1: Read x2 - value 98 at site 1")

        self.assertTrue("T1" in self.transaction_manager.sites_transactions_read_write_log)
        self.assertEquals(self.transaction_manager.sites_transactions_read_write_log["T1"], \
                          set(self.transaction_manager.sites.keys()))

        self.assertTrue("T1" in self.transaction_manager.sites_transactions_accessed_log)
        self.assertEquals(self.transaction_manager.sites_transactions_accessed_log["T1"], \
                          set(self.transaction_manager.sites.values()))

        end_t1 = parser.get_instruction()
        self.assertEquals(end_t1.instruction_type, InstructionType.END)
        self.assertEquals(end_t1.transaction_identifier, "T1")

        with std_out() as (out, err):
            self.transaction_manager.execute(end_t1)

        output = out.getvalue().strip()
        self.assertEquals(output, "T1 committed")

        self.assertEquals(self.transaction_manager.transactions["T1"].state, TransactionState.COMMITTED)
        self.assertEquals(self.transaction_manager.transactions["T1"].transaction_type, TransactionType.READ_WRITE)

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


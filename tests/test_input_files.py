# -*- coding: utf-8 -*-
""" Test Data Manager """
import unittest
#from src.objects.site import Site
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

class DataManagerTestCase(unittest.TestCase):
    """ Test cases for the Data Manager """

    def setUp(self):
        self.logger = Logger()
        self.transaction_manager = TransactionManager(self.logger)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.input_dir = dir_path.replace("/tests", "/input_files")

    def tearDown(self):
        self.transaction_manager = None

    def test_input_1(self):
        """ Test the first input file """

        parser = Parser(self.input_dir + "/input_1", self.logger)

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
                self.assertEquals(variable.value, 10)
                self.assertEquals(variable.written_values[0], 10)

                self.assertTrue("x1" in site.data_manager.locks)
                self.assertTrue("T1" in site.data_manager.entries)
                self.assertTrue("x1" in site.data_manager.entries["T1"])
                self.assertEquals(site.data_manager.entries["T1"]["x1"].written_values[DEFAULT_START_TIME], 10)
                self.assertTrue("T1" in self.transaction_manager.sites_transactions_read_write_log)
            else:
                self.assertFalse("x1" in site.data_manager.variables)
                self.assertFalse("x1" in site.data_manager.locks)

        self.assertEquals(self.transaction_manager.sites_transactions_read_write_log["T1"], set([2]))
        self.assertTrue("T1" in self.transaction_manager.sites_transactions_accessed_log)
        self.assertEquals(self.transaction_manager.sites_transactions_accessed_log["T1"], \
                        set([self.transaction_manager.sites[2]]))

        write_t2_x2 = parser.get_instruction()
        self.assertEquals(write_t2_x2.instruction_type, InstructionType.WRITE)
        self.assertEquals(write_t2_x2.transaction_identifier, "T2")
        self.assertEquals(write_t2_x2.variable_identifier, "x2")
        self.assertEquals(write_t2_x2.value, "202")

        self.transaction_manager.execute(write_t2_x2)
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
            self.assertEquals(variable.value, 20)
            self.assertEquals(variable.written_values[0], 20)

            self.assertTrue("x2" in site.data_manager.locks)
            self.assertTrue("T2" in site.data_manager.entries)
            self.assertTrue("x2" in site.data_manager.entries["T2"])
            self.assertEquals(site.data_manager.entries["T2"]["x2"].written_values[DEFAULT_START_TIME], 20)

        self.assertTrue("T2" in self.transaction_manager.sites_transactions_read_write_log)
        self.assertEquals(self.transaction_manager.sites_transactions_read_write_log["T2"], \
                          set(self.transaction_manager.sites.keys()))

        self.assertTrue("T2" in self.transaction_manager.sites_transactions_accessed_log)
        self.assertEquals(self.transaction_manager.sites_transactions_accessed_log["T2"], \
                            set(self.transaction_manager.sites.values()))

        write_t1_x2 = parser.get_instruction()
        self.assertEquals(write_t1_x2.instruction_type, InstructionType.WRITE)
        self.assertEquals(write_t1_x2.transaction_identifier, "T1")
        self.assertEquals(write_t1_x2.variable_identifier, "x2")
        self.assertEquals(write_t1_x2.value, "102")

        self.transaction_manager.execute(write_t1_x2)
        self.assertEquals(self.transaction_manager.transactions["T1"].state, \
                          TransactionState.BLOCKED)

        self.assertTrue("T2" in self.transaction_manager.blocked_transactions_instructions_map)
        instruction = self.transaction_manager.blocked_transactions_instructions_map["T2"][0]
        self.assertEquals(instruction.instruction_type, InstructionType.WRITE)
        self.assertEquals(instruction.variable_identifier, "x2")
        self.assertEquals(instruction.transaction_identifier, "T1")
        self.assertEquals(instruction.value, "102")

        for site_id, site in self.transaction_manager.sites.iteritems():
            self.assertEquals(site.status, SiteStatus.UP)

            self.assertTrue("x2" in site.data_manager.variables)
            variable = site.data_manager.variables["x2"]
            self.assertEquals(variable.index, 2)
            self.assertEquals(variable.identifier, "x2")
            self.assertEquals(variable.replicated, True)
            self.assertEquals(variable.readable, True)
            self.assertEquals(variable.value, 20)
            self.assertEquals(variable.written_values[0], 20)

            self.assertTrue("x2" in site.data_manager.locks)
            if site_id == 2:
                self.assertTrue("T1" in site.data_manager.entries) # From first write
                self.assertFalse("x2" in site.data_manager.entries["T1"])
            else:
                self.assertFalse("T1" in site.data_manager.entries) # From first write

        self.assertTrue("T1" in self.transaction_manager.sites_transactions_read_write_log)
        self.assertEquals(self.transaction_manager.sites_transactions_read_write_log["T1"], \
                          set([2])) # From the initial write

        self.assertTrue("T1" in self.transaction_manager.sites_transactions_accessed_log)
        self.assertEquals(self.transaction_manager.sites_transactions_accessed_log["T1"], \
                            set([self.transaction_manager.sites[2]]))

        write_t2_x1 = parser.get_instruction()
        self.assertEquals(write_t2_x1.instruction_type, InstructionType.WRITE)
        self.assertEquals(write_t2_x1.transaction_identifier, "T2")
        self.assertEquals(write_t2_x1.variable_identifier, "x1")
        self.assertEquals(write_t2_x1.value, "201")

        self.transaction_manager.execute(write_t2_x1)
        self.assertEquals(self.transaction_manager.transactions["T2"].state, \
                          TransactionState.ABORTED)

        self.assertEquals(self.transaction_manager.transactions["T1"].state, \
                          TransactionState.RUNNING)

        self.assertFalse("T1" in self.transaction_manager.blocked_transactions_instructions_map)
        self.assertFalse("T2" in self.transaction_manager.blocked_transactions_instructions_map)
        self.assertEquals(self.transaction_manager.transactions["T2"].state, TransactionState.ABORTED)
        self.assertEquals(self.transaction_manager.transactions["T1"].state, TransactionState.RUNNING)

        for site_id, site in self.transaction_manager.sites.iteritems():
            self.assertEquals(site.status, SiteStatus.UP)

            self.assertTrue("x2" in site.data_manager.variables)
            variable = site.data_manager.variables["x2"]
            self.assertEquals(variable.index, 2)
            self.assertEquals(variable.identifier, "x2")
            self.assertEquals(variable.replicated, True)
            self.assertEquals(variable.readable, True)
            self.assertEquals(variable.value, 20)
            self.assertEquals(variable.written_values[0], 20)

            self.assertTrue("x2" in site.data_manager.locks)
            self.assertEquals(site.data_manager.locks["x2"][0].transaction.identifier, "T1")

            self.assertTrue("T1" in site.data_manager.entries)
            if site_id == 2:
                self.assertTrue("x1" in site.data_manager.entries["T1"])
            else:
                self.assertFalse("x1" in site.data_manager.entries["T1"])

            self.assertTrue("x2" in site.data_manager.entries["T1"])

        self.assertTrue("T1" in self.transaction_manager.sites_transactions_read_write_log)
        self.assertEquals(self.transaction_manager.sites_transactions_read_write_log["T1"], \
                          set(self.transaction_manager.sites.keys()))

        self.assertFalse("T2" in self.transaction_manager.sites_transactions_read_write_log)

        self.assertTrue("T1" in self.transaction_manager.sites_transactions_accessed_log)
        self.assertEquals(self.transaction_manager.sites_transactions_accessed_log["T1"], \
                            set(self.transaction_manager.sites.values()))
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

        self.assertTrue(len(self.transaction_manager.sites_transactions_accessed_log) == 0)

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


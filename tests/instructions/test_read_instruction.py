# -*- coding: utf-8 -*-
""" Test Read Operation """
import unittest
import sys
from contextlib import contextmanager
from StringIO import StringIO
from src.objects.instruction import Instruction
from src.objects.site import SiteStatus
from src.transaction_manager import TransactionManager, TransactionType
from src.utilities.logger import Logger

class ReadOperationTestCase(unittest.TestCase):
    """ Test to ensure the correctness of the Read Method """

    def setUp(self):
        logger = Logger()
        self.trans_manager = TransactionManager(logger)

    def test_read_instruction_with_no_transaction(self):
        """ Ensure a Transaction was started before a read is attempted """
        instruction = Instruction("R(T3,x4)")

        self.assertRaises(ValueError, self.trans_manager.execute, instruction)

    def test_first_time_read_instruction(self):
        """ Ensure a read lock is obtained and the correct value is read """
        trans_identifer = "T1"
        variable_identifier = "x1"
        site_id = 2
        begin = Instruction("begin(%s)" % trans_identifer)
        self.trans_manager.execute(begin)

        # Confirm transaction was created and added to list of Transactions
        self.assertTrue(trans_identifer in self.trans_manager.transactions)

        self.assertEquals(self.trans_manager.transactions[trans_identifer].transaction_type, \
                          TransactionType.READ_WRITE)

        # Confirm that the variable does exist
        self.assertTrue(len(self.trans_manager.variables_to_site_map[variable_identifier]) > 0)

        # Confirm all sites are up
        for site in self.trans_manager.sites.values():
            self.assertTrue(site.status == SiteStatus.UP)

        read = Instruction("R(%s,%s)" % (trans_identifer, variable_identifier))
        with std_out() as (out, err):
            self.trans_manager.execute(read)

        output = out.getvalue().strip()
        self.assertEquals(output, "Read %s: 10 at site %i" % (variable_identifier, site_id))

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

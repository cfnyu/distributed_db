# -*- coding: utf-8 -*-
""" Test End Transaction Operation """
import unittest
import sys
from contextlib import contextmanager
from StringIO import StringIO
from src.objects.instruction import Instruction
from src.objects.site import SiteStatus
from src.objects.lock import Lock, LockType
from src.transaction_manager import TransactionManager, TransactionType
from src.utilities.logger import Logger

class EndTransactionOperationTestCase(unittest.TestCase):
    """ Test to ensure the correctness of the End Transaction Method """

    def setUp(self):
        logger = Logger()
        self.trans_manager = TransactionManager(logger)

    def test_a_transaction_can_be_ended(self):
        """ Ensure that a simple transaction can be ended """

        begin = Instruction("begin(T1)")
        self.trans_manager.execute(begin)

        self.assertTrue("T1" in self.trans_manager.transactions)

        read = Instruction("R(T1,x2)")
        self.trans_manager.execute(read)

        site_list = []
        for site in self.trans_manager.sites_transactions_accessed_log["T1"]:
            site_list.append(site.identifer)

        # All sites should have been visited and obtained a read lock
        for site_id, site in self.trans_manager.sites.iteritems():
            self.assertTrue(site_id in site_list)
            for lock in site.data_manager.locks["x2"]:
                self.assertTrue(lock.lock_type == LockType.READ)
                self.assertTrue(lock.transaction.identifier == "T1")

        transaction = self.trans_manager.transactions["T1"]

        with std_out() as (out, err):
            self.trans_manager.end_transaction(transaction)

        output = out.getvalue().strip()
        self.assertTrue(output == "Transaction T1 committed successfully")
        
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


# -*- coding: utf-8 -*-
""" Test Data Manager """
import unittest
#from src.objects.site import Site
from src.objects.instruction import Instruction
from src.objects.lock import Lock, LockType
from src.objects.transaction import Transaction, TransactionType
from src.objects.variable import Variable
from src.sites.data_manager import DataManager
from src.utilities.logger import Logger

class DataManagerTestCase(unittest.TestCase):
    """ Test cases for the Data Manager """

    def setUp(self):
        logger = Logger()
        # logger.show_stdout()
        self.data_manager = DataManager()
        site_id = 1

        # Load all variables
        for i in range(1, 21):
            if i % 2 == 0 or 1 + (i % 10) == site_id:
                logger.log("Adding " + str(Variable(i)))
                self.data_manager.add_variable(1, Variable(i))

    def test_obtain_read_lock_with_no_existing_locks(self):
        """ Test that a lock can be obtained when no locks exist """

        transaction = Transaction("T1", TransactionType.READ_WRITE, 1)
        instruction = Instruction("R(T1, x2)")
        self.assertEquals(instruction.variable_identifier, "x2")
        variable = self.data_manager.variables["x2"]

        self.assertTrue(variable.readable)
        self.assertFalse("x2" in self.data_manager.locks)

        value = self.data_manager.obtain_read_lock(transaction, instruction)
        self.assertEquals(len(self.data_manager.locks), 1)
        self.assertTrue(value)

    def test_obtain_read_lock_with_existing_locks(self):
        """ Test that a lock can be obtained when other locks exist """

        dummy_tran = Transaction("T3", TransactionType.READ_WRITE, 1)
        dummy_var = Variable(4)
        dummy_var1 = Variable(6)

        self.data_manager.locks["x4"] = [Lock(LockType.READ, dummy_tran, dummy_var)]
        self.data_manager.locks["x6"] = [Lock(LockType.WRITE, dummy_tran, dummy_var1)]

        transaction = Transaction("T1", TransactionType.READ_WRITE, 1)
        instruction = Instruction("R(T1, x2)")
        variable = self.data_manager.variables["x2"]

        self.assertTrue(variable.readable)
        self.assertFalse("x2" in self.data_manager.locks)

        value = self.data_manager.obtain_read_lock(transaction, instruction)
        self.assertTrue("x2" in self.data_manager.locks)
        self.assertTrue(value)

    def test_obtain_read_lock_when_variable_unreadable(self):
        """ Test that a lock cannot be obtained when the Variable Readable is set to False """

        transaction = Transaction("T1", TransactionType.READ_WRITE, 1)
        instruction = Instruction("R(T1, x2)")
        variable = self.data_manager.variables["x2"]
        variable.readable = False
        self.data_manager.variables["x2"] = variable
        self.assertFalse(self.data_manager.variables["x2"].readable)
        self.assertFalse(self.data_manager.obtain_read_lock(transaction, instruction))

    def test_obtain_read_lock_with_ro_transaction(self):
        """ Test that a lock can be obtained when the Transaction Is Read-Only """

        transaction = Transaction("T1", TransactionType.READ_ONLY, 1)
        instruction = Instruction("R(T1, x2)")

        self.assertTrue(transaction.transaction_type == TransactionType.READ_ONLY)
        self.assertTrue(self.data_manager.obtain_read_lock(transaction, instruction))

    def test_obtain_read_lock_with_existing_read_lock(self):
        """ Test that a lock cannot be obtained when another Transaction has a lock """

        transaction = Transaction("T1", TransactionType.READ_WRITE, 1)
        instruction = Instruction("R(T1, x2)")

        self.assertTrue(self.data_manager.obtain_read_lock(transaction, instruction))
        self.assertEquals(self.data_manager.locks["x2"][0].lock_type, LockType.READ)
        self.assertEquals(self.data_manager.locks["x2"][0].transaction.index, 1)

        transaction = Transaction("T2", TransactionType.READ_WRITE, 1)
        instruction = Instruction("R(T2, x2)")

        self.assertTrue("x2" in self.data_manager.locks)
        self.assertTrue(self.data_manager.obtain_read_lock(transaction, instruction))

    def test_obtain_read_lock_with_existing_write_lock(self):
        """ Test that a lock cannot be obtained when another Transaction has a lock """

        transaction = Transaction("T1", TransactionType.READ_WRITE, 1)
        instruction = Instruction("W(T1,x2, 103)")
        self.data_manager.locks["x2"] = [Lock(LockType.WRITE, transaction, instruction)]

        transaction = Transaction("T2", TransactionType.READ_WRITE, 1)
        instruction = Instruction("R(T2, x2)")

        self.assertTrue("x2" in self.data_manager.locks)
        self.assertFalse(self.data_manager.obtain_read_lock(transaction, instruction))

    def test_obtain_read_lock_when_trans_has_exiting_lock(self):
        """ Test that a lock can be obtained when same Transaction requests the same lock """

        transaction = Transaction("T1", TransactionType.READ_WRITE, 1)
        instruction = Instruction("R(T2, x2)")
        self.assertTrue(self.data_manager.obtain_read_lock(transaction, instruction))

        self.assertTrue("x2" in self.data_manager.locks)
        self.assertTrue(self.data_manager.obtain_read_lock(transaction, instruction))

    def test_read_with_no_locks(self):
        """ Test the read method, which should return the last committed value """

        transaction = Transaction("T1", TransactionType.READ_WRITE, 1)
        instruction = Instruction("R(T1, x2)")

        self.assertEquals(self.data_manager.read(transaction, instruction), 20)

    @unittest.skip("NEEDS TO BE IMPLEMENTED")
    def test_read_with_after_transaction_has_a_write(self):
        """ Ensure the lastest submitted value for the current transaction is returned """

        transaction = Transaction("T1", TransactionType.READ_WRITE, 1)
        instruction = Instruction("R(T1, x2)")

        self.assertEquals(self.data_manager.read(transaction, instruction), 20)

# -*- coding: utf-8 -*-
""" Test Logger Class """
import unittest

from src.utilities.logger import log, init_logger

class LoggerTestCase(unittest.TestCase):
    """ Test cases for Logger """

    def test_no_output_verbose_false(self):
        """ Test that no output is shown to stdout when Verbose flag is False """

        self.assertEquals(log("Something"), 0)

    def test_prints_when_verbose_true(self):
        """ Test that output is shown to stdout when Verbose flag is True """
        init_logger(True)
        self.assertNotEquals(log("Something"), 0)

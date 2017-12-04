# -*- coding: utf-8 -*-
""" Test Logger Class """
import unittest

from src.utilities.logger import Logger

class LoggerTestCase(unittest.TestCase):
    """ Test cases for Logger """

    def test_no_output_verbose_false(self):
        """ Test that no output is shown to stdout when Verbose flag is False """
        logger = Logger()

        self.assertEquals(logger.log("Something"), 0)

    def test_prints_when_verbose_true(self):
        """ Test that output is shown to stdout when Verbose flag is True """

        logger = Logger()
        logger.show_stdout()
        self.assertNotEquals(logger.log("Something"), 0)

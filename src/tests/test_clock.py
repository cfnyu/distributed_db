# -*- coding: utf-8 -*-
""" Test Clock Class """
import unittest

from src.objects.clock import Clock

class ClockTestCase(unittest.TestCase):
    """ Test cases for Clock class """

    def test_clock(self):
        """ Test that clock is working """
        clock = Clock()

        clock.tick()
        self.assertEquals(clock.time, 1)

        clock.tick()
        self.assertEquals(clock.time, 2)

    def test_show_clock_output(self):
        clock = Clock()

        self.assertEquals(str(clock), "<Time: 0>")
# -*- coding: utf-8 -*-
""" Test Site Class """
import unittest

from src.objects.site import Site
from src.sites.data_manager import DataManager
from src.sites.lock_manager import LockManager
class SiteTestCase(unittest.TestCase):
    """ Test cases for a single Site """

    def test_site_value(self):
        """ Test that returns it's Id  """

        dm = DataManager()
        lm = LockManager()
        site = Site(1, dm, lm)

        self.assertTrue("1" in str(site))

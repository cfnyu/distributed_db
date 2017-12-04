# -*- coding: utf-8 -*-
""" Test Site Class """
import unittest

from src.objects.site import Site
from src.utilities.logger import Logger

class SiteTestCase(unittest.TestCase):
    """ Test cases for a single Site """

    def setUp(self):
        self.logger = Logger()
        self.logger.show_stdout()

    def test_variables_on_site_one(self):
        """ Confirm which variables are on Site 1 """
        site = Site(1, self.logger)

        self.confirm_even_variables_are_present(site)
        self.confirm_odd_variables_are_not_present(site)

    def test_variables_on_site_two(self):
        """ Confirm which variables are on Site 2 """
        site = Site(2, self.logger)

        self.confirm_even_variables_are_present(site)

        self.assertTrue("x1" in site.data_manager.variables)
        self.assertTrue("x11" in site.data_manager.variables)

        # No other odd variables should be on site one
        self.assertFalse("x3" in site.data_manager.variables)
        self.assertFalse("x5" in site.data_manager.variables)
        self.assertFalse("x7" in site.data_manager.variables)
        self.assertFalse("x9" in site.data_manager.variables)
        self.assertFalse("x13" in site.data_manager.variables)
        self.assertFalse("x15" in site.data_manager.variables)
        self.assertFalse("x17" in site.data_manager.variables)
        self.assertFalse("x19" in site.data_manager.variables)


    def test_variables_on_site_three(self):
        """ Confirm which variables are on Site 3 """
        site = Site(3, self.logger)

        self.confirm_even_variables_are_present(site)
        self.confirm_odd_variables_are_not_present(site)

    def test_variables_on_site_four(self):
        """ Confirm which variables are on Site 4 """
        site = Site(4, self.logger)

        self.confirm_even_variables_are_present(site)

        self.assertTrue("x3" in site.data_manager.variables)
        self.assertTrue("x13" in site.data_manager.variables)
        
        self.assertFalse("x1" in site.data_manager.variables)
        self.assertFalse("x11" in site.data_manager.variables)
        self.assertFalse("x5" in site.data_manager.variables)
        self.assertFalse("x15" in site.data_manager.variables)
        self.assertFalse("x7" in site.data_manager.variables)
        self.assertFalse("x17" in site.data_manager.variables)
        self.assertFalse("x9" in site.data_manager.variables)
        self.assertFalse("x19" in site.data_manager.variables)

    def test_variables_on_site_five(self):
        """ Confirm which variables are on Site 5 """
        site = Site(5, self.logger)

        self.confirm_even_variables_are_present(site)
        self.confirm_odd_variables_are_not_present(site)

    def test_variables_on_site_six(self):
        """ Confirm which variables are on Site 6 """
        site = Site(6, self.logger)

        self.confirm_even_variables_are_present(site)
        self.assertTrue("x5" in site.data_manager.variables)
        self.assertTrue("x15" in site.data_manager.variables)

        self.assertFalse("x1" in site.data_manager.variables)
        self.assertFalse("x11" in site.data_manager.variables)
        self.assertFalse("x3" in site.data_manager.variables)
        self.assertFalse("x13" in site.data_manager.variables)
        self.assertFalse("x7" in site.data_manager.variables)
        self.assertFalse("x17" in site.data_manager.variables)
        self.assertFalse("x9" in site.data_manager.variables)
        self.assertFalse("x19" in site.data_manager.variables)

    def test_variables_on_site_seven(self):
        """ Confirm which variables are on Site 7 """
        site = Site(7, self.logger)

        self.confirm_even_variables_are_present(site)
        self.confirm_odd_variables_are_not_present(site)

    def test_variables_on_site_eight(self):
        """ Confirm which variables are on Site 8 """
        site = Site(8, self.logger)

        self.confirm_even_variables_are_present(site)

        self.assertTrue("x7" in site.data_manager.variables)
        self.assertTrue("x17" in site.data_manager.variables)
        
        self.assertFalse("x1" in site.data_manager.variables)
        self.assertFalse("x11" in site.data_manager.variables)
        self.assertFalse("x3" in site.data_manager.variables)
        self.assertFalse("x13" in site.data_manager.variables)
        self.assertFalse("x5" in site.data_manager.variables)
        self.assertFalse("x15" in site.data_manager.variables)
        self.assertFalse("x9" in site.data_manager.variables)
        self.assertFalse("x19" in site.data_manager.variables)

    def test_variables_on_site_nine(self):
        """ Confirm which variables are on Site 9 """
        site = Site(9, self.logger)

        self.confirm_even_variables_are_present(site)
        self.confirm_odd_variables_are_not_present(site)

    def test_variables_on_site_ten(self):
        """ Confirm which variables are on Site 10 """
        site = Site(10, self.logger)

        self.confirm_even_variables_are_present(site)

        self.assertTrue("x9" in site.data_manager.variables)
        self.assertTrue("x19" in site.data_manager.variables)

        self.assertFalse("x1" in site.data_manager.variables)
        self.assertFalse("x11" in site.data_manager.variables)
        self.assertFalse("x3" in site.data_manager.variables)
        self.assertFalse("x13" in site.data_manager.variables)
        self.assertFalse("x5" in site.data_manager.variables)
        self.assertFalse("x15" in site.data_manager.variables)
        self.assertFalse("x7" in site.data_manager.variables)
        self.assertFalse("x17" in site.data_manager.variables)

    def test_variables_on_site_eleven(self):
        """ Confirm which variables are on Site 11 """
        site = Site(11, self.logger)

        self.confirm_even_variables_are_present(site)
        self.confirm_odd_variables_are_not_present(site)

    def test_variables_on_site_twelve(self):
        """ Confirm which variables are on Site 12 """
        site = Site(12, self.logger)

        self.confirm_even_variables_are_present(site)
        self.confirm_odd_variables_are_not_present(site)

    def test_variables_on_site_thirteen(self):
        """ Confirm which variables are on Site 13 """
        site = Site(13, self.logger)

        self.confirm_even_variables_are_present(site)
        self.confirm_odd_variables_are_not_present(site)

    def test_variables_on_site_fourteen(self):
        """ Confirm which variables are on Site 14 """
        site = Site(14, self.logger)

        self.confirm_even_variables_are_present(site)
        self.confirm_odd_variables_are_not_present(site)

    def test_variables_on_site_fifteen(self):
        """ Confirm which variables are on Site 15 """
        site = Site(15, self.logger)

        self.confirm_even_variables_are_present(site)
        self.confirm_odd_variables_are_not_present(site)

    def test_variables_on_site_sixteen(self):
        """ Confirm which variables are on Site 16 """
        site = Site(16, self.logger)

        self.confirm_even_variables_are_present(site)
        self.confirm_odd_variables_are_not_present(site)

    def test_variables_on_site_seventeen(self):
        """ Confirm which variables are on Site 17 """
        site = Site(17, self.logger)

        self.confirm_even_variables_are_present(site)
        self.confirm_odd_variables_are_not_present(site)

    def test_variables_on_site_eighteen(self):
        """ Confirm which variables are on Site 18 """
        site = Site(18, self.logger)

        self.confirm_even_variables_are_present(site)
        self.confirm_odd_variables_are_not_present(site)

    def test_variables_on_site_nineteen(self):
        """ Confirm which variables are on Site 19 """
        site = Site(19, self.logger)

        self.confirm_even_variables_are_present(site)
        self.confirm_odd_variables_are_not_present(site)

    def test_variables_on_site_twenty(self):
        """ Confirm which variables are on Site 20 """
        site = Site(20, self.logger)

        self.confirm_even_variables_are_present(site)
        self.confirm_odd_variables_are_not_present(site)

    def confirm_even_variables_are_present(self, site):
        """ Even variables should be on all Sites """

        self.assertTrue("x2" in site.data_manager.variables)
        self.assertTrue("x4" in site.data_manager.variables)
        self.assertTrue("x6" in site.data_manager.variables)
        self.assertTrue("x8" in site.data_manager.variables)
        self.assertTrue("x10" in site.data_manager.variables)
        self.assertTrue("x12" in site.data_manager.variables)
        self.assertTrue("x14" in site.data_manager.variables)
        self.assertTrue("x16" in site.data_manager.variables)
        self.assertTrue("x18" in site.data_manager.variables)
        self.assertTrue("x20" in site.data_manager.variables)

    def confirm_odd_variables_are_not_present(self, site):
        """ Odd variables should be on specific Sites only """
        
        self.assertFalse("x1" in site.data_manager.variables)
        self.assertFalse("x11" in site.data_manager.variables)
        self.assertFalse("x3" in site.data_manager.variables)
        self.assertFalse("x13" in site.data_manager.variables)
        self.assertFalse("x5" in site.data_manager.variables)
        self.assertFalse("x15" in site.data_manager.variables)
        self.assertFalse("x7" in site.data_manager.variables)
        self.assertFalse("x17" in site.data_manager.variables)
        self.assertFalse("x9" in site.data_manager.variables)
        self.assertFalse("x19" in site.data_manager.variables)
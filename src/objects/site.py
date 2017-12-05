# -*- coding: utf-8 -*-
""" Site

This module represents a site

"""
from src.sites.data_manager import DataManager
from src.objects.variable import Variable
from enum import Enum

class SiteStatus(Enum):
    """ Represents the possible status of a Site """
    UP = 1,
    DOWN = 2

class Site:
    """ Represents a single Site """

    def __init__(self, site_id, time, logger):
        self.identifer = site_id
        self.data_manager = DataManager()
        self.status = SiteStatus.UP

        # Load all variables
        for i in range(1, 21):
            if i % 2 == 0 or 1 + (i % 10) == site_id:
                logger.log("Adding " + str(Variable(i)))
                self.data_manager.add_variable(time, Variable(i))

    def dump(self):
        """ Dump the results of all commits values to stdout """

        print self.data_manager.variables

    def recover(self):
        """ Recover this site """
        pass

    def fail(self):
        """ Fail this site """
        pass

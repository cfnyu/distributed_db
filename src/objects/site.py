# -*- coding: utf-8 -*-
""" Site

This module represents a site

"""
from enum import Enum
from sites.data_manager import DataManager
from objects.variable import Variable

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
        self.create_time = 0

        # Load all variables
        for i in range(1, 21):
            if i % 2 == 0 or 1 + (i % 10) == site_id:
                logger.log("Adding " + str(Variable(i)) + " at time "+ str(time))
                self.data_manager.add_variable(time, Variable(i))

    def dump(self):
        """ Dump the results of all commits values to stdout """

        return self.data_manager.variables

    def recover(self):
        """ Recover this site """
        pass

    def fail(self):
        """ Fail this site """
        pass

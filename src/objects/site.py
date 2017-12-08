# -*- coding: utf-8 -*-
""" Site

This module represents a site

"""
from enum import IntEnum
from sites.data_manager import DataManager
from objects.variable import Variable

class SiteStatus(IntEnum):
    """ Represents the possible status of a Site """
    UP = 1,
    DOWN = 2

class Site:
    """ Represents a single Site """

    def __init__(self, site_id, time, logger):
        self.identifer = site_id # TODO: Fix typo
        self.status = SiteStatus.UP
        self.create_time = 0
        variables = {}

        # Load all variables
        for i in range(1, 21):
            if i % 2 == 0 or 1 + (i % 10) == site_id:
                new_variable = Variable(time, i)
                logger.log("Adding %s at time %s" % (new_variable.identifier, str(time)))
                variables[new_variable.identifier] = new_variable

        self.data_manager = DataManager(variables, logger, site_id)

    def dump(self):
        """ Dump the results of all commits values to stdout """

        return self.data_manager.variables

    def recover(self, time):
        """ Recover this site """

        self.status = SiteStatus.UP
        self.create_time = time

        for variable in self.data_manager.variables.values():
            variable.readable = not variable.replicated
           
    def fail(self):
        """ Fail this site """
        self.status = SiteStatus.DOWN
        #clear lock list
        self.data_manager.locks = {}
        self.data_manager.entries = {}  # clear entries log

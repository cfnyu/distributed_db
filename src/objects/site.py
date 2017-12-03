# -*- coding: utf-8 -*-
""" Site

This module represents a site

"""

class Site:
    """ Represents a single Site """

    def __init__(self, site_id, data_manager, lock_manager):
        self.id = site_id
        self.data_manager = data_manager
        self.lock_manager = lock_manager

    def __repr__(self):
        return "<Site: %i>" % self.id
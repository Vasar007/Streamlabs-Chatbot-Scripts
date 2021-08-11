# -*- coding: utf-8 -*-


class SongRequestManager(object):

    def __init__(self, parent_wrapper, settings, logger):
        self.parent_wrapper = parent_wrapper
        self.settings = settings
        self.logger = logger

    def add_request(self):
        ...

    def cancel_request(self):
        ...

    def approve_request(self):
        ...

    def reject_request(self):
        ...

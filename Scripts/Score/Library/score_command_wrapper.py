# -*- coding: utf-8 -*-

import score_helpers as helpers


class ScoreCommandWrapper(object):

    def __init__(self, command, func, required_permission):
        self.command = str(command)
        self.func = func
        self.required_permission = required_permission

    def has_func(self):
        return self.func is not None

    def has_required_permission(self):
        return self.required_permission is not None

    def is_unknown_command(self):
        return not self.has_func() and not self.has_required_permission()

    def __str__(self):
        return self.command

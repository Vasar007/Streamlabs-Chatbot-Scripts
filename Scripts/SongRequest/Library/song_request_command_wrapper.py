# -*- coding: utf-8 -*-


class SongRequestCommandWrapper(object):

    def __init__(self, command, func, required_permission, is_valid_call,
                 usage_example):
        self.command = str(command)
        self.func = func
        self.required_permission = required_permission
        self.is_valid_call = is_valid_call
        self.usage_example = usage_example

    def has_func(self):
        return self.func is not None

    def has_required_permission(self):
        return self.required_permission is not None

    def is_unknown_command(self):
        return not self.has_func() and not self.has_required_permission()

    def is_invalid_command_call(self):
        return self.is_unknown_command() or not self.is_valid_call

    def __str__(self):
        return self.command

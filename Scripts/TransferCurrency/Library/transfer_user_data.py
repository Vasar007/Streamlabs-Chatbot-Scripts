# -*- coding: utf-8 -*-


class TransferUserData(object):

    def __init__(self, user_id, user_name):
        self.id = user_id
        self.name = user_name

    def has_id(self):
        return bool(self.id)

    def has_name(self):
        return bool(self.name)

    def is_empty(self):
        return not self.has_id() or not self.has_name()

    @staticmethod
    def empty():
        return TransferUserData(None, None)

    def __str__(self):
        return "{0}: {1}".format(self.id, self.name)

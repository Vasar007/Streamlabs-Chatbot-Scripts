# -*- coding: utf-8 -*-


class TransferUserData(object):

    def __init__(self, user_id, user_name):
        self.id = user_id
        self.name = user_name

    def has_id(self):
        return bool(self.id)

    def has_name(self):
        return bool(self.name)

    def has_value(self):
        return self.has_id() or self.has_name()

    @staticmethod
    def empty():
        return TransferUserData(None, None)

    def __bool__(self):
        return self.has_value()

    def __str__(self):
        return "{0}: {1}".format(self.id, self.name)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (
            isinstance(other, TransferUserData) and
            self.id == other.id
        )

    def __ne__(self, other):
        return not self.__eq__(other)

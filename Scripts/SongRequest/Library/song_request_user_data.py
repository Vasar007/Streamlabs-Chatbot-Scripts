# -*- coding: utf-8 -*-


class SongRequestUserData(object):

    def __init__(self, user_id, user_name):
        self.id = user_id
        self.name = user_name

    def has_id(self):
        return bool(self.id)

    def has_name(self):
        return bool(self.name)

    def is_empty(self):
        return not self.has_id() and not self.has_name()

    @staticmethod
    def empty():
        return SongRequestUserData(None, None)

    def __bool__(self):
        return not self.is_empty()

    def __str__(self):
        return "{0}: {1}".format(self.id, self.name)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (
            isinstance(other, SongRequestUserData) and
            self.id == other.id
        )

    def __ne__(self, other):
        return not self.__eq__(other)

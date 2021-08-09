# -*- coding: utf-8 -*-


class SongRequestUserName(object):

    def __init__(self, user_name):
        self.user_name = user_name

    def __str__(self):
        return self.user_name

    def __hash__(self) -> int:
        return hash(self.user_name)

    def __eq__(self, other):
        return (
            isinstance(other, SongRequestUserName) and
            self.user_name == other.user_name
        )

    def __ne__(self, other):
        return not self.__eq__(other)


class SongRequestUserId(object):

    def __init__(self, user_id):
        self.user_id = user_id

    def __str__(self):
        return self.user_id

    def __hash__(self) -> int:
        return hash(self.user_id)

    def __eq__(self, other):
        return (
            isinstance(other, SongRequestUserId) and
            self.user_id == other.user_id
        )

    def __ne__(self, other):
        return not self.__eq__(other)

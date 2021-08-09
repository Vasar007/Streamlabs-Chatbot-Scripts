# -*- coding: utf-8 -*-

from Scripts.Score.score_config import Description
import uuid


class SongRequestState(object):
    WaitingForApproval = 1
    ApprovedAndPending = 2
    ApprovedAndAddedSuccessfully = 3
    ApprovedButAddedFailure = 4
    Rejected = 5
    Cancelled = 6


class SongRequest(object):

    def __init__(self, user_id, song_link, number, state):
        self.user_id = user_id
        self.song_link = song_link
        self.number = number
        self.state = state

        self.id = uuid.uuid4()

    def __str__(self):
        return (
            "request ID {0}, user ID {1}, song link {2}, number {3}, " +
            "state {4}".format(
                self.id, self.user_id, self.song_link, self.number, self.state 
            )
        )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other):
        return (
            isinstance(other, SongRequest) and
            self.id == other.id
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def create_new(user_id, song_link, number):
        return SongRequest(
            user_id, song_link, number, SongRequestState.WaitingForApproval
        )

    def approve(self):
        self.state = SongRequestState.ApprovedAndPending

    def add_to_queue(self):
        self.state = SongRequestState.ApprovedAndAddedSuccessfully

    def fail_to_add(self):
        self.state = SongRequestState.ApprovedButAddedFailure

    def reject(self):
        self.state = SongRequestState.Rejected

    def cancel(self):
        self.state = SongRequestState.Cancelled


class SongRequestResult(object):

    def __init__(self, song_request, description=None):
        self.song_request = song_request
        self.description = description

    @staticmethod
    def successful(song_request):
        song_request.add_to_queue()
        return SongRequestResult(song_request, description=None)

    @staticmethod
    def failed(song_request, description):
        song_request.fail_to_add()
        return SongRequestResult(song_request, description)

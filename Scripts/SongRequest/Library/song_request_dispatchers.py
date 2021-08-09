# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from song_request import SongRequestState


class BaseSongRequestDispatcher(object):

    __metaclass__ = ABCMeta

    def __init__(self, parent_wrapper, settings, logger, storage):
        self.parent_wrapper = parent_wrapper
        self.settings = settings
        self.logger = logger
        self.storage = storage

    @abstractmethod
    def dispatch(self):
        raise NotImplementedError()


class PendingSongRequestDispatcher(BaseSongRequestDispatcher):

    def __init__(self, parent_wrapper, settings, logger, storage):
        super(PendingSongRequestDispatcher, self).__init__(
            parent_wrapper, settings, logger, storage
        )

    def dispatch(self):
        denied_requests = self.storage.get_requests_with_states(
            SongRequestState.ApprovedAndPending
        )

        for request in denied_requests:
            self.logger.info("Pending request [{0}].".format(request))


class DeniedSongRequestDispatcher(BaseSongRequestDispatcher):

    def __init__(self, parent_wrapper, settings, logger, storage):
        super(PendingSongRequestDispatcher, self).__init__(
            parent_wrapper, settings, logger, storage
        )

    def dispatch(self):
        denied_requests = self.storage.get_requests_with_states(
            SongRequestState.Rejected,
            SongRequestState.Cancelled
        )

        for request in denied_requests:
            self.logger.info("Denied request [{0}].".format(request))

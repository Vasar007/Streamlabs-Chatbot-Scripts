# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from Scripts.SongRequest.CSharp.Models.Requests import SongRequestState
from Scripts.SongRequest.CSharp.Models.Requests import SongRequestResult


class BaseSongRequestDispatcher(object):

    __metaclass__ = ABCMeta

    def __init__(self, parent_wrapper, settings, logger):
        self.parent_wrapper = parent_wrapper
        self.settings = settings
        self.logger = logger

    @abstractmethod
    def dispatch(self, storage):
        raise NotImplementedError()


class PendingSongRequestDispatcher(BaseSongRequestDispatcher):

    def __init__(self, parent_wrapper, settings, logger, page_scrapper):
        super(PendingSongRequestDispatcher, self).__init__(
            parent_wrapper, settings, logger
        )
        self.page_scrapper = page_scrapper

    def dispatch(self, storage):
        pending_requests = storage.get_requests_with_states(
            SongRequestState.ApprovedAndPending
        )

        if not pending_requests:
            self.logger.debug("No pending requests found. Skipping dispatch.")
            return

        # Update request's states to prevent double processing.
        for i in range (len(pending_requests)):
            request = pending_requests[i]
            request = request.StartProcessing()
            pending_requests[i] = request

        storage.update_states(pending_requests)

        # Star real processing of requests.
        for request in pending_requests:
            self._process_request(request)

        storage.update_states(pending_requests)

    def _process_request(self, request):
        self.logger.info("Processing request [{0}].".format(request))

        result = None
        try:
            result = self.page_scrapper.Process(request)
        except Exception as ex:
            error = str(ex)
            self.logger.exception(
                "Failed to process request {0}: {1}"
                .format(request.Id, error)
            )
            result = SongRequestResult.Fail(request, error)

        self._handle_result(result)

    def _handle_result(self, result):
        self.logger.info("Processing request result [{0}].".format(result))

        message = None
        user_name = result.SongRequest.UserData.Name.Value
        description = result.Description
        if result.IsSuccess:
            if description:
                description = " {0}".format(result.Description)

            message = (
                self.settings.OnSuccessSongRequestMessage
                .format(user_name, description)
            )
        else:
            if not description:
                description = self.settings.OnFailureSongRequestDefaultErrorMessage

            message = (
                self.settings.OnFailureSongRequestMessage
                .format(user_name, description)
            )

        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)


class DeniedSongRequestDispatcher(BaseSongRequestDispatcher):

    def __init__(self, parent_wrapper, settings, logger):
        super(DeniedSongRequestDispatcher, self).__init__(
            parent_wrapper, settings, logger
        )

    def dispatch(self, storage):
        denied_requests = storage.get_requests_with_states(
            SongRequestState.Rejected,
            SongRequestState.Cancelled
        )

        for request in denied_requests:
            self.logger.info("Denied request [{0}].".format(request))
            storage.remove_request(request)
            self.logger.info(
                "Denied request {0} was removed from storage."
                .format(request.Id)
            )

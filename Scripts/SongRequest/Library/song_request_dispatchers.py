# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

import song_request_config as config

from System import DateTime
from Scripts.SongRequest.CSharp.Models.Requests import SongRequestState
from Scripts.SongRequest.CSharp.Models.Requests import SongRequestResult


def format_song_request(song_link, request_number):
    return config.SongRequestNumberAndLinkFormat.format(
        request_number, song_link
    )


class BaseSongRequestDispatcher(object):

    __metaclass__ = ABCMeta

    def __init__(self, parent_wrapper, settings, logger):
        self.parent_wrapper = parent_wrapper
        self.settings = settings
        self.logger = logger

    @abstractmethod
    def dispatch(self, storage):
        raise NotImplementedError()


class WaitingSongRequestDispatcher(BaseSongRequestDispatcher):

    def __init__(self, parent_wrapper, settings, logger):
        super(WaitingSongRequestDispatcher, self).__init__(
            parent_wrapper, settings, logger
        )

    def dispatch(self, storage):
        waiting_requests = storage.get_requests_with_states(
            SongRequestState.WaitingForApproval
        )

         # Update request's states if waiting timeout has passed.
        for i in range (len(waiting_requests)):
            request = waiting_requests[i]
            request = self._process_request(request)
            waiting_requests[i] = request

        storage.update_states(waiting_requests)

    def _process_request(self, request):
        self.logger.debug("Waiting request [{0}].".format(request))

        request_creation_time = request.CreationTimeUtc
        current_time = DateTime.UtcNow
        waiting_timeout_in_seconds = self.settings.WaitingTimeoutForSongRequestsInSeconds

        if current_time < request_creation_time.AddSeconds(waiting_timeout_in_seconds):
            self.logger.debug(
                "Waiting timeout has not passed for request {0}."
                .format(request.RequestId)
            )
            return request

        self.logger.info(
            "Waiting request {0} was approved because timeout has passed."
            .format(request.RequestId)
        )
        return request.Approve()



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

        # Start real processing of requests.
        for i in range (len(pending_requests)):
            request = pending_requests[i]
            pending_requests[i] = self._process_request(request)

        storage.update_states(pending_requests)

    def _process_request(self, request):
        self.logger.debug("Processing request [{0}].".format(request))

        result = None
        try:
            result = self.page_scrapper.Process(request)
        except Exception as ex:
            error = str(ex)
            self.logger.exception(
                "Failed to process request {0}: {1}"
                .format(request.RequestId, error)
            )
            result = SongRequestResult.Fail(request, error)

        return self._handle_result(result)

    def _handle_result(self, result):
        self.logger.info("Processing request result [{0}].".format(result))

        user_name = result.SongRequest.UserData.Name.Value
        description = result.Description
        song_request_with_number = format_song_request(
            result.SongRequest.SongLink.Value,
            result.SongRequest.RequestNumber.Value
        )

        message = None
        if result.IsSuccess:
            if not description:
                description = self.settings.OnSuccessSongRequestDefaultResultMessage

            message = (
                self.settings.OnSuccessSongRequestMessage
                .format(user_name, song_request_with_number, description)
            )
        else:
            if not description:
                description = self.settings.OnFailureSongRequestDefaultErrorMessage

            message = (
                self.settings.OnFailureSongRequestMessage
                .format(user_name, song_request_with_number, description)
            )

        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

        return result.SongRequest


class DeniedSongRequestDispatcher(BaseSongRequestDispatcher):

    def __init__(self, parent_wrapper, settings, logger):
        super(DeniedSongRequestDispatcher, self).__init__(
            parent_wrapper, settings, logger
        )

    def dispatch(self, storage):
        denied_requests = storage.get_requests_with_states(
            SongRequestState.ApprovedButAddedFailure,
            SongRequestState.Rejected,
            SongRequestState.Canceled
        )

        for request in denied_requests:
            self._process_request(request, storage)

    def _process_request(self, request, storage):
        self.logger.debug("Denied request [{0}].".format(request))

        storage.remove_request(request)
        self.logger.info(
            "Denied request {0} was removed from storage."
            .format(request.RequestId)
        )

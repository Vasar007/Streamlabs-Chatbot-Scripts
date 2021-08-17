# -*- coding: utf-8 -*-

import time

from abc import ABCMeta, abstractmethod

import song_request_config as config

from System import DateTime
from Scripts.SongRequest.CSharp.Models.Requests import SongRequestState
from Scripts.SongRequest.CSharp.Models.Requests import SongRequestResult


def format_song_request(settings, request):
    return settings.SongRequestNumberAndLinkFormat.format(
        request.RequestNumber.Value, request.SongLink.Value
    )


def format_processed_song_request(settings, request):
    if request.ProcessedBy is None:
        return format_song_request(settings, request)

    submessage = (
        "{0}, {1}"
        .format(
            request.ProcessedBy.UserData.Name.Value,
            request.ProcessedBy.ProcessedTimeUtcAsString,
        )
    )
    if request.ProcessedBy.Reason:
        submessage += ", " + request.ProcessedBy.Reason

    return settings.ProcessedSongRequestNumberAndLinkFormat.format(
        request.RequestNumber.Value,
        request.SongLink.Value,
        request.State,
        submessage
    )


class BaseSongRequestDispatcher(object):

    __metaclass__ = ABCMeta

    def __init__(self, parent_wrapper, settings, logger):
        self._parent_wrapper = parent_wrapper
        self._settings = settings
        self._logger = logger

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
        self._logger.debug("Waiting request [{0}].".format(request))

        request_creation_time = request.CreationTimeUtc
        current_time = DateTime.UtcNow
        waiting_timeout_in_seconds = self._settings.WaitingTimeoutForSongRequestsInSeconds

        if current_time < request_creation_time.AddSeconds(waiting_timeout_in_seconds):
            self._logger.debug(
                "Waiting timeout has not passed for request {0}."
                .format(request.RequestId)
            )
            return request

        self._logger.info(
            "Waiting request {0} was approved because timeout has passed."
            .format(request.RequestId)
        )
        return request.AutoApprove(self._settings.AutoApproveReason)



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
            self._logger.debug("No pending requests found. Skipping dispatch.")
            return

        # Update request's states to prevent double processing.
        len_pending_requests = len(pending_requests)
        for i in range(len_pending_requests):
            request = pending_requests[i]
            request = request.StartProcessing()
            pending_requests[i] = request

        storage.update_states(pending_requests)

        # Start real processing of requests.
        for i in range(len_pending_requests):
            request = pending_requests[i]
            pending_requests[i] = self._process_request(request)

            # Need to wait some time before new request processing.
            if len_pending_requests > 1:
                self._logger.debug("Waiting some time before new request.")
                time.sleep(self._settings.TimeoutToWaitBetweenSongRequestsInSeconds)

        storage.update_states(pending_requests)

    def _process_request(self, request):
        self._logger.debug("Processing request [{0}].".format(request))

        result = None
        try:
            result = self.page_scrapper.Process(request)
        except Exception as ex:
            error = str(ex)
            self._logger.exception(
                "Failed to process request {0}: {1}"
                .format(request.RequestId, error)
            )
            result = SongRequestResult.Fail(request, error)

        return self._handle_result(result)

    def _handle_result(self, result):
        self._logger.debug("Processing request result [{0}].".format(result))

        user_name = result.SongRequest.UserData.Name.Value
        description = result.Description
        song_request_with_number = format_processed_song_request(
            self._settings,
            result.SongRequest
        )

        message = None
        if result.IsSuccess:
            if not description:
                description = self._settings.OnSuccessSongRequestDefaultResultMessage

            message = (
                self._settings.OnSuccessSongRequestMessage
                .format(user_name, song_request_with_number, description)
            )
        else:
            if not description:
                description = self._settings.OnFailureSongRequestDefaultErrorMessage

            message = (
                self._settings.OnFailureSongRequestMessage
                .format(user_name, song_request_with_number, description)
            )

        self._logger.info(message)
        self._parent_wrapper.send_stream_message(message)

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
        self._logger.debug("Denied request [{0}].".format(request))

        storage.remove_request(request)
        self._logger.info(
            "Denied request {0} was removed from storage."
            .format(request.RequestId)
        )

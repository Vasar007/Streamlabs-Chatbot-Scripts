# -*- coding: utf-8 -*-

import song_request_config as config
import song_request_helpers as helpers

from song_request_storage import SongRequestStorage as Storage
from song_request_user_searcher import SongRequestUserSearcher as UserSearcher

from song_request_dispatchers import format_song_request
from song_request_dispatchers import PendingSongRequestDispatcher
from song_request_dispatchers import DeniedSongRequestDispatcher

from Scripts.SongRequest.CSharp.Models.Requests import SongRequestNumber
from Scripts.SongRequest.CSharp.Models.Requests import SongRequestModel
from Scripts.SongRequest.CSharp.Models.Requests import SongRequestDecision


class SongRequestManager(object):

    def __init__(self, parent_wrapper, settings, logger, dispatchers):
        self.parent_wrapper = parent_wrapper
        self.settings = settings
        self.logger = logger

        self.storage = Storage(logger)
        self.searcher = UserSearcher(parent_wrapper, logger)

        self.dispatchers = dispatchers

    def run_dispatch(self):
        for dispatcher in self.dispatchers:
            dispatcher.dispatch(self.storage)

    def add_request(self, user_data, song_link):
        self.logger.debug(
            "Adding request from user [{0}], link [{1}]."
            .format(user_data, song_link)
        )

        # Here we should have only processed or pending requests.
        # Nor rejected neither cancelled requets should be here.
        user_requests = self.storage.get_user_requests(user_data.Id)
        number_of_requests = len(user_requests)
        if number_of_requests >= self.settings.MaxNumberOfSongRequestsToAdd:
            self._handle_limit_exceeded(user_data.Name.Value)
            return False

        number = SongRequestNumber(number_of_requests + 1)
        request = SongRequestModel.CreateNew(user_data, song_link, number)
        self.storage.add_request(request)

        song_request_with_number = format_song_request(
            song_link.Value, number.Value
        )
        self._handle_request_added(user_data.Name.Value, song_request_with_number)
        self._handle_request_to_approve(user_data.Name.Value, song_request_with_number)
        return True

    def cancel_request(self):
        raise NotImplementedError()

    def approve_request(self, request_decision):
        self.logger.debug(
            "Approving request with decision [{0}].".format(request_decision)
        )

        return self._internal_processing(
            request_decision,
            lambda request: request.Approve(),
            self._handle_request_approved
        )

    def reject_request(self, request_decision):
        self.logger.debug(
            "Rejecting request with decision [{0}].".format(request_decision)
        )

        return self._internal_processing(
            request_decision,
            lambda request: request.Reject(),
            self._handle_request_rejected
        )

    def _prepare_target_data(self, request_decision):
        # Retrive data about user.
        target_data = self.searcher.find_user_data(
            request_decision.TargetUserIdOrName.Value
        )
        if not target_data.HasValue:
            self._handle_invalid_target(
                request_decision.UserData.Name.Value,
                request_decision.TargetUserIdOrName.Value
            )
            # "target_data" == UserData.Empty here.
            return target_data

        return target_data

    def _get_target_requests_to_use(self, request_decision):
        target_data = self._prepare_target_data(request_decision)
        if not target_data.HasValue:
            self.logger.debug(
                "Target user {0} is invalid, interupt song request processing."
                .format(request_decision.TargetUserIdOrName.Value)
            )
            return None

        target_user_requests = self.storage.get_user_requests(target_data.Id)
        if not target_user_requests:
            self._handle_no_requests(
                request_decision.UserData.Name.Value,
                request_decision.TargetUserIdOrName.Value
            )
            return None

        target_user_requests_to_use = target_user_requests
        if not request_decision.RequestNumber.IsAll:
            if len(target_user_requests) < request_decision.RequestNumber.Value:
                self._handle_nonexistent_request_number(
                    request_decision.UserData.Name.Value,
                    request_decision.TargetUserIdOrName.Value,
                    request_decision.RequestNumber.Value
                )
                return None

            index_to_use = request_decision.RequestNumber.Value - 1
            target_user_requests_to_use = [target_user_requests[index_to_use]]

        return target_user_requests_to_use

    def _internal_processing(self, request_decision, process_func,
                             handle_func):
        target_user_requests_to_use = self._get_target_requests_to_use(
            request_decision
        )
        if not target_user_requests_to_use:
            return False

        for i in range(len(target_user_requests_to_use)):
            request = target_user_requests_to_use[i]
            if request.IsWaitingForApproval:
                target_user_requests_to_use[i] = process_func(request)

                song_request_with_number = format_song_request(
                    request.SongLink.Value, request.RequestNumber.Value
                )

                handle_func(
                    request_decision.UserData.Name.Value,
                    request_decision.TargetUserIdOrName.Value,
                    song_request_with_number,
                    request_decision.Reason
                )

        self.storage.update_states(target_user_requests_to_use)
        return True

    def _handle_limit_exceeded(self, user_name):
        message = (
            self.settings.MaxLimitOfSongRequestsIsExceededMessage
            .format(user_name, self.settings.MaxNumberOfSongRequestsToAdd)
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def _handle_request_added(self, user_name, song_request):
        message = (
            self.settings.SongRequestAddedMessage
            .format(user_name, song_request)
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def _handle_request_to_approve(self, user_name, song_request):
        message = (
            self.settings.SongRequestToApproveMessage
            .format(
                song_request,
                user_name,
                self.settings.CommandApproveSongRequest,
                self.settings.CommandRejectSongRequest
            )
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def _handle_invalid_target(self, user_name, target):
        message = (
            self.settings.InvalidTargetMessage
            .format(user_name, target)
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def _handle_no_requests(self, user_name, target):
        message = (
            self.settings.NoSongRequestsMessage
            .format(user_name, target)
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def _handle_nonexistent_request_number(self, user_name, target,
                                           invalid_number):
        message = (
            self.settings.NonExistentSongRequestNumberMessage
            .format(user_name, invalid_number, target)
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def _format_with_reason(self, message, reason):
        if reason:
            text_reason = (
                self.settings.SongRequestDecisionReasonMessage.format(reason)
            )
            return "{0} {1}".format(message, text_reason)

        return message

    def _handle_request_approved(self, user_name, target, song_request,
                                 reason):
        message = (
            self.settings.SongRequestApprovedMessage
            .format(target, song_request, user_name)
        )
        message = self._format_with_reason(message, reason)

        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def _handle_request_rejected(self, user_name, target, song_request,
                                 reason):
        message = (
            self.settings.SongRequestRejectedMessage
            .format(target, song_request, user_name)
        )
        message = self._format_with_reason(message, reason)

        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)


def create_manager(parent_wrapper, settings, logger, page_scrapper):
    dispatchers = [
        PendingSongRequestDispatcher(parent_wrapper, settings, logger, page_scrapper),
        DeniedSongRequestDispatcher(parent_wrapper, settings, logger)
    ]
    manager = SongRequestManager(parent_wrapper, settings, logger, dispatchers)
    return manager


def approve_or_reject_request(command, data_wrapper, settings, manager):
    user_data = helpers.wrap_user_data(
        data_wrapper.user_id, data_wrapper.user_name
    )

    raw_target_user_id_or_name = data_wrapper.get_param(1)
    target_user_id_or_name = helpers.wrap_user_id_or_name(
        raw_target_user_id_or_name
    )
    param_count = data_wrapper.get_param_count()

    request_number = SongRequestNumber.All
    if param_count > 1:
        raw_request_number = data_wrapper.get_param(2)
        request_number = SongRequestNumber.TryParse(
            raw_request_number, SongRequestNumber.All
        )

    reason = ""
    if param_count > 1:
        seems_like_request_number = data_wrapper.get_param(2)
        is_request_number = (
            seems_like_request_number.isdigit() or
            seems_like_request_number == SongRequestNumber.RawAllValue
        )
        if param_count > 2:
            start_reason = 2 if not is_request_number else 3
            for i in range(start_reason, param_count):
                reason += " " + data_wrapper.get_param(i)

    request_decision = SongRequestDecision(
        user_data, target_user_id_or_name, request_number, reason
    )

    if command == settings.CommandApproveSongRequest:
        manager.approve_request(request_decision)
    elif command == settings.CommandRejectSongRequest:
        manager.reject_request(request_decision)
    else:
        raise ValueError("Unexpected command to handle: {0}.".format(command))

# -*- coding: utf-8 -*-

import threading

import song_request_config as config
import song_request_helpers as helpers

from song_request_storage import SongRequestStorage as Storage
from song_request_user_searcher import SongRequestUserSearcher as UserSearcher
from song_request_messenger import SongRequestMessengerHandler as MessengerHandler

from song_request_dispatchers import format_song_request
from song_request_dispatchers import format_processed_song_request
from song_request_dispatchers import PendingSongRequestDispatcher
from song_request_dispatchers import WaitingSongRequestDispatcher
from song_request_dispatchers import DeniedSongRequestDispatcher

from song_request_settings import SongRequestCSharpSettings as CSharpSettings

from Scripts.SongRequest.CSharp.Models.Requests import SongRequestNumber
from Scripts.SongRequest.CSharp.Models.Requests import SongRequestModel
from Scripts.SongRequest.CSharp.Models.Requests import SongRequestDecision


class SongRequestManager(object):

    def __init__(self, settings, logger, searcher, messenger, dispatchers):
        self._settings = settings
        self._logger = logger
        self._messenger = messenger
        self._searcher = searcher
        self._dispatchers = dispatchers

        self._storage = Storage(logger)
        self._lock = threading.Lock()

    def get_messenger(self):
        return self._messenger

    def run_dispatch(self):
        if self._lock.locked():
            self._logger.debug(
                "Cannot do dispatch because another dispatch is running."
            )
            return

        with self._lock:
            self._logger.debug("Running dispatch iteration.")
            for dispatcher in self._dispatchers:
                dispatcher.dispatch(self._storage)

    def get_user_requests_for(self, user_data, target_user_id_or_name):
        self._logger.debug(
            "Getting all requests from user [{0}]."
            .format(target_user_id_or_name)
        )

        target_data = self._prepare_target_data(
            user_data, target_user_id_or_name
        )
        if not target_data.HasValue:
            self._logger.debug(
                "Target user {0} is invalid, skip user requests processing."
                .format(target_user_id_or_name)
            )
            return (None, None)

        return (self._get_user_requests(target_data), target_data)

    def remove_all_user_requests_for(self, user_data, target_user_id_or_name):
        self._logger.debug(
            "Removing all requests for user [{0}]."
            .format(target_user_id_or_name)
        )

        target_data = self._prepare_target_data(
            user_data, target_user_id_or_name
        )
        if not target_data.HasValue:
            self._logger.debug(
                "Target user {0} is invalid, skip user requests processing."
                .format(target_user_id_or_name)
            )
            return None

        all_target_user_requests = self._get_user_requests(target_data)
        for request in all_target_user_requests:
            self._storage.remove_request(request)

        return target_data

    def add_request(self, user_data, song_link):
        self._logger.debug(
            "Adding request from user [{0}], link [{1}]."
            .format(user_data, song_link)
        )

        user_requests = self._get_user_requests(user_data)
        number_of_requests = len(user_requests)
        if number_of_requests >= self._settings.MaxNumberOfSongRequestsToAdd:
            self._handle_limit_exceeded(
                user_data.Id.Value, user_data.Name.Value
            )
            return False

        number = SongRequestNumber(number_of_requests + 1)
        request = SongRequestModel.CreateNew(user_data, song_link, number)
        self._storage.add_request(request)

        song_request_with_number = format_song_request(
            self._settings, request
        )

        self._handle_request_added(
            user_data.Id.Value, user_data.Name.Value, song_request_with_number
        )

        self._handle_request_to_approve(
            user_data.Name.Value, song_request_with_number
        )

        return True

    def cancel_request(self, request_decision):
        self._logger.debug(
            "Canceling request with decision [{0}].".format(request_decision)
        )

        return self._internal_processing(
            request_decision,
            lambda request: request.Cancel(request_decision),
            self._handle_request_canceled
        )

    def approve_request(self, request_decision):
        self._logger.debug(
            "Approving request with decision [{0}].".format(request_decision)
        )

        return self._internal_processing(
            request_decision,
            lambda request: request.Approve(request_decision),
            self._handle_request_approved
        )

    def reject_request(self, request_decision):
        self._logger.debug(
            "Rejecting request with decision [{0}].".format(request_decision)
        )

        return self._internal_processing(
            request_decision,
            lambda request: request.Reject(request_decision),
            self._handle_request_rejected
        )

    def _prepare_target_data(self, user_data, target_user_id_or_name):
        # Retrieve data about user.
        target_data = self._searcher.find_user_data(
            target_user_id_or_name.Value
        )
        if not target_data.HasValue:
            self._handle_invalid_target(
                user_data.Id.Value,
                user_data.Name.Value,
                target_user_id_or_name.Value
            )
            # "target_data" == UserData.Empty here.
            return target_data

        return target_data

    def _get_target_requests_to_use(self, request_decision):
        target_data = self._prepare_target_data(
            request_decision.UserData, request_decision.TargetUserIdOrName
        )
        if not target_data.HasValue:
            self._logger.debug(
                "Target user {0} is invalid, interrupt song request processing."
                .format(request_decision.TargetUserIdOrName.Value)
            )
            return None

        all_target_user_requests = self._get_user_requests(target_data)
        target_user_requests = [
            request for request in all_target_user_requests
            if request.IsWaitingForApproval
        ]
        if not target_user_requests:
            self._handle_no_requests(
                request_decision.UserData.Id.Value,
                request_decision.UserData.Name.Value,
                target_data.Name.Value
            )
            return None

        target_user_requests_to_use = target_user_requests
        if not request_decision.RequestNumber.IsAll:
            if len(all_target_user_requests) < request_decision.RequestNumber.Value:
                self._handle_nonexistent_request_number(
                    request_decision.UserData.Id.Value,
                    request_decision.UserData.Name.Value,
                    target_data.Name.Value,
                    request_decision.RequestNumber.Value
                )
                return None

            index_to_use = request_decision.RequestNumber.Value - 1
            selected_request = all_target_user_requests[index_to_use]
            if not selected_request.IsWaitingForApproval:
                self._handle_already_processed_request(
                    request_decision.UserData.Id.Value,
                    request_decision.UserData.Name.Value,
                    target_data.Name.Value,
                    selected_request
                )
                return None

            target_user_requests_to_use = [selected_request]

        return target_user_requests_to_use

    def _get_user_requests(self, user_data):
        self._logger.debug(
            "Getting all requests from user [{0}].".format(user_data)
        )

        # Here we should have only processed or pending requests.
        # Neither rejected nor canceled request should be here.
        return self._storage.get_user_requests(user_data.Id)

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

                # Here we have specific format, so, we do not need extended
                # format for processed requests.
                song_request_with_number = format_song_request(
                    self._settings, request
                )

                handle_func(
                    request_decision.UserData.Name.Value,
                    request.UserData.Id.Value,
                    request.UserData.Name.Value,
                    song_request_with_number,
                    request_decision.Reason
                )

        self._storage.update_states(target_user_requests_to_use)
        return True

    def _handle_limit_exceeded(self, user_id, user_name):
        message = (
            self._settings.MaxLimitOfSongRequestsIsExceededMessage
            .format(user_name, self._settings.MaxNumberOfSongRequestsToAdd)
        )
        self._logger.info(message)
        self._messenger.send_message(user_id, message)

    def _handle_request_added(self, user_id, user_name, song_request):
        if self._settings.LowMessageMode:
            return

        message = (
            self._settings.SongRequestAddedMessage
            .format(user_name, song_request)
        )
        self._logger.info(message)
        self._messenger.send_message(user_id, message)

    def _handle_request_to_approve(self, user_name, song_request):
        if self._settings.LowMessageMode:
            return

        message = (
            self._settings.SongRequestToApproveMessage
            .format(
                song_request,
                user_name,
                self._settings.CommandApproveSongRequest,
                self._settings.CommandRejectSongRequest
            )
        )

        self._logger.info(message)
        mod_ids = self._settings.parse_mod_ids(self._logger)
        self._messenger.send_message_for_group(mod_ids, message)

    def _handle_invalid_target(self, user_id, user_name, target):
        message = (
            self._settings.InvalidTargetMessage
            .format(user_name, target)
        )
        self._logger.info(message)
        self._messenger.send_message(user_id, message)

    def _handle_no_requests(self, user_id, user_name, target):
        message = (
            self._settings.NoSongRequestsMessage
            .format(user_name, target)
        )
        self._logger.info(message)
        self._messenger.send_message(user_id, message)

    def _handle_nonexistent_request_number(self, user_id, user_name,
                                           target_name, invalid_number):
        message = (
            self._settings.NonExistentSongRequestNumberMessage
            .format(user_name, invalid_number, target_name)
        )
        self._logger.info(message)
        self._messenger.send_message(user_id, message)

    def _handle_already_processed_request(self, user_id, user_name,
                                          target_name, selected_request):
        submessage = format_processed_song_request(
            self._settings, selected_request
        )
        message = (
            self._settings.AlreadyProcessedSongRequestMessage
            .format(user_name, target_name, submessage)
        )
        self._logger.info(message)
        self._messenger.send_message(user_id, message)

    def _format_with_reason(self, message, reason):
        if reason:
            text_reason = (
                self._settings.SongRequestDecisionReasonMessage.format(reason)
            )
            return "{0} {1}".format(message, text_reason)

        return message

    def _handle_request_canceled(self, user_name, target_id, target_name,
                                 song_request, reason):
        message = (
            self._settings.SongRequestCancelMessage
            .format(target_name, song_request)
        )
        message = self._format_with_reason(message, reason)

        self._logger.info(message)
        self._messenger.send_message(target_id, message)

    def _handle_request_approved(self, user_name, target_id, target_name,
                                 song_request, reason):
        message = (
            self._settings.SongRequestApprovedMessage
            .format(target_name, song_request, user_name)
        )
        message = self._format_with_reason(message, reason)

        self._logger.info(message)
        self._messenger.send_message(target_id, message)

    def _handle_request_rejected(self, user_name, target_id, target_name,
                                 song_request, reason):
        message = (
            self._settings.SongRequestRejectedMessage
            .format(target_name, song_request, user_name)
        )
        message = self._format_with_reason(message, reason)

        self._logger.info(message)
        self._messenger.send_message(target_id, message)


def create_manager(parent_wrapper, settings, logger, page_scrapper):
    searcher = UserSearcher(parent_wrapper, logger)
    messenger = MessengerHandler(parent_wrapper, settings, logger)
    dispatchers = [
        PendingSongRequestDispatcher(parent_wrapper, settings, logger, page_scrapper),
        WaitingSongRequestDispatcher(parent_wrapper, settings, logger),
        DeniedSongRequestDispatcher(parent_wrapper, settings, logger)
    ]
    return SongRequestManager(
        settings,
        logger,
        searcher,
        messenger,
        dispatchers
    )


def cancel_request(data_wrapper, settings, manager):
    user_data = helpers.wrap_user_data(
        data_wrapper.user_id, data_wrapper.user_name
    )

    # User can cancel request only for yourself.
    target_user_id_or_name = helpers.wrap_user_id_or_name(
        data_wrapper.user_id
    )

    param_count = data_wrapper.get_param_count()
    param_number_to_process = 1

    request_number = SongRequestNumber.All
    if param_count > 1:
        raw_request_number = data_wrapper.get_param(param_number_to_process)
        request_number = SongRequestNumber.TryParse(
            raw_request_number, SongRequestNumber.All, CSharpSettings(settings)
        )

    reason = ""
    if param_count > 1:
        seems_like_request_number = data_wrapper.get_param(
            param_number_to_process
        )
        is_request_number = (
            seems_like_request_number.isdigit() or
            settings.is_all_parameter(seems_like_request_number)
        )
        start_reason = 1 if not is_request_number else 2
        for i in range(start_reason, param_count):
            reason += " " + data_wrapper.get_param(i)
        reason = reason.strip()

    request_decision = SongRequestDecision.CreateWithUtcNow(
        user_data, target_user_id_or_name, request_number, reason
    )

    manager.cancel_request(request_decision)


def approve_or_reject_request(command, data_wrapper, settings, manager):
    user_data = helpers.wrap_user_data(
        data_wrapper.user_id, data_wrapper.user_name
    )

    raw_target_user_id_or_name = helpers.strip_at_symbol_for_name(
        data_wrapper.get_param(1)
    )
    target_user_id_or_name = helpers.wrap_user_id_or_name(
        raw_target_user_id_or_name
    )

    param_number_to_process = 2
    param_count = data_wrapper.get_param_count()

    request_number = SongRequestNumber.All
    if param_count > 1:
        raw_request_number = data_wrapper.get_param(param_number_to_process)
        request_number = SongRequestNumber.TryParse(
            raw_request_number, SongRequestNumber.All, CSharpSettings(settings)
        )

    reason = ""
    if param_count > 1:
        seems_like_request_number = data_wrapper.get_param(
            param_number_to_process
        )
        is_request_number = (
            seems_like_request_number.isdigit() or
            settings.is_all_parameter(seems_like_request_number)
        )
        if param_count > 2:
            start_reason = 2 if not is_request_number else 3
            for i in range(start_reason, param_count):
                reason += " " + data_wrapper.get_param(i)
            reason = reason.strip()
        elif not is_request_number:
            reason = seems_like_request_number

    request_decision = SongRequestDecision.CreateWithUtcNow(
        user_data, target_user_id_or_name, request_number, reason
    )

    if command == settings.CommandApproveSongRequest:
        manager.approve_request(request_decision)
    elif command == settings.CommandRejectSongRequest:
        manager.reject_request(request_decision)
    else:
        raise ValueError("Unexpected command to handle: {0}.".format(command))


def change_option_for_user(data_wrapper, settings, logger, manager):
    second_subcommand = data_wrapper.get_param(3).lower()

    if settings.is_reset_subcommand(second_subcommand):
        reset_option_for_user(data_wrapper, settings, logger, manager)
    else:
        message = (
            settings.InvalidOptionsSubcommandMessage
            .format(data_wrapper.user_name, second_subcommand)
        )
        logger.info(message)
        manager.get_messenger().send_message(data_wrapper.user_id, message)


def reset_option_for_user(data_wrapper, settings, logger, manager):
    user_data = helpers.wrap_user_data(
        data_wrapper.user_id, data_wrapper.user_name
    )

    raw_target_user_id_or_name = helpers.strip_at_symbol_for_name(
        data_wrapper.get_param(2)
    )
    target_user_id_or_name = helpers.wrap_user_id_or_name(
        raw_target_user_id_or_name
    )

    target_data = manager.remove_all_user_requests_for(
        user_data, target_user_id_or_name
    )

    if target_data:
        target_user_name = target_data.Name.Value
        message = (
            settings.ResetUserSongRequestOptionsMessage
            .format(target_user_name, user_data.Name.Value)
        )
        logger.info(message)
        manager.get_messenger().send_message(user_data.Id.Value, message)


def get_all_user_requests(data_wrapper, settings, logger, manager):
    user_data = helpers.wrap_user_data(
        data_wrapper.user_id, data_wrapper.user_name
    )

    raw_target_user_id_or_name = helpers.strip_at_symbol_for_name(
        data_wrapper.get_param(1)
    )
    target_user_id_or_name = helpers.wrap_user_id_or_name(
        raw_target_user_id_or_name
    )

    (user_requests, target_data) = manager.get_user_requests_for(
        user_data, target_user_id_or_name
    )

    target_user_name = None
    if target_data:
        target_user_name = target_data.Name.Value
    else:
        target_user_name = target_user_id_or_name.Value

    message = None
    if user_requests:
        map_lambda = lambda request: format_processed_song_request(
            settings, request
        )
        processed_requests = map(map_lambda, user_requests)
        formatted_requests = (
            "{0} ".format(config.DefaultDelimeter).join(processed_requests)
        )

        message = (
            settings.GotUserSongRequestsMessage
            .format(
                target_user_name,
                len(user_requests),
                formatted_requests
            )
        )
    else:
        message = (
            settings.NoUserSongRequestsMessage
            .format(target_user_name)
        )

    logger.info(message)
    manager.get_messenger().send_message(user_data.Id.Value, message)

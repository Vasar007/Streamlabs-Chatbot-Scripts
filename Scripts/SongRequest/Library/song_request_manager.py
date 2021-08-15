# -*- coding: utf-8 -*-

import song_request_config as config
import song_request_helpers as helpers

from song_request_storage import SongRequestStorage as Storage
from song_request_user_searcher import SongRequestUserSearcher as UserSearcher
from song_request_messenger import SongRequestMessengerHandler as MessengerHandler

from song_request_dispatchers import format_song_request
from song_request_dispatchers import PendingSongRequestDispatcher
from song_request_dispatchers import WaitingSongRequestDispatcher
from song_request_dispatchers import DeniedSongRequestDispatcher

from Scripts.SongRequest.CSharp.Models.Requests import SongRequestNumber
from Scripts.SongRequest.CSharp.Models.Requests import SongRequestModel
from Scripts.SongRequest.CSharp.Models.Requests import SongRequestDecision


class SongRequestManager(object):

    def __init__(self, settings, logger, searcher, messenger, dispatchers):
        self.settings = settings
        self.logger = logger
        self.messenger = messenger
        self.searcher = searcher
        self.dispatchers = dispatchers

        self.storage = Storage(logger)

    def get_messenger(self):
        return self.messenger

    def run_dispatch(self):
        for dispatcher in self.dispatchers:
            dispatcher.dispatch(self.storage)

    def get_user_requests_for(self, user_data, target_user_id_or_name):
        self.logger.debug(
            "Getting all requests from user [{0}]."
            .format(target_user_id_or_name)
        )

        target_data = self._prepare_target_data(
            user_data, target_user_id_or_name
        )
        if not target_data.HasValue:
            self.logger.debug(
                "Target user {0} is invalid, skip user requests processing."
                .format(request_decision.TargetUserIdOrName.Value)
            )
            return None

        return self._get_user_requests(target_data)

    def add_request(self, user_data, song_link):
        self.logger.debug(
            "Adding request from user [{0}], link [{1}]."
            .format(user_data, song_link)
        )

        user_requests = self._get_user_requests(user_data)
        number_of_requests = len(user_requests)
        if number_of_requests >= self.settings.MaxNumberOfSongRequestsToAdd:
            self._handle_limit_exceeded(user_data.Id.Value)
            return False

        number = SongRequestNumber(number_of_requests + 1)
        request = SongRequestModel.CreateNew(user_data, song_link, number)
        self.storage.add_request(request)

        song_request_with_number = format_song_request(
            song_link.Value, number.Value
        )

        self._handle_request_added(
            user_data.Id.Value, song_request_with_number
        )

        self._handle_request_to_approve(
            user_data.Name.Value, song_request_with_number
        )

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

    def _prepare_target_data(self, user_data, target_user_id_or_name):
        # Retrieve data about user.
        target_data = self.searcher.find_user_data(
            target_user_id_or_name.Value
        )
        if not target_data.HasValue:
            self._handle_invalid_target(
                user_data.Id.Value,
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
            self.logger.debug(
                "Target user {0} is invalid, interrupt song request processing."
                .format(request_decision.TargetUserIdOrName.Value)
            )
            return None

        target_user_requests = self._get_user_requests(target_data)
        if not target_user_requests:
            self._handle_no_requests(
                request_decision.UserData.Id.Value,
                request_decision.TargetUserIdOrName.Value
            )
            return None

        target_user_requests_to_use = target_user_requests
        if not request_decision.RequestNumber.IsAll:
            if len(target_user_requests) < request_decision.RequestNumber.Value:
                self._handle_nonexistent_request_number(
                    request_decision.UserData.Id.Value,
                    request_decision.TargetUserIdOrName.Value,
                    request_decision.RequestNumber.Value
                )
                return None

            index_to_use = request_decision.RequestNumber.Value - 1
            target_user_requests_to_use = [target_user_requests[index_to_use]]

        return target_user_requests_to_use

    def _get_user_requests(self, user_data):
        self.logger.debug(
            "Getting all requests from user [{0}].".format(user_data)
        )

        # Here we should have only processed or pending requests.
        # Neither rejected nor canceled request should be here.
        return self.storage.get_user_requests(user_data.Id)

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
                    request.UserData.Id.Value,
                    song_request_with_number,
                    request_decision.Reason
                )

        self.storage.update_states(target_user_requests_to_use)
        return True

    def _handle_limit_exceeded(self, user_id):
        message = (
            self.settings.MaxLimitOfSongRequestsIsExceededMessage
            .format(user_id, self.settings.MaxNumberOfSongRequestsToAdd)
        )
        self.logger.info(message)
        self.messenger.send_message(user_id, message)

    def _handle_request_added(self, user_id, song_request):
        message = (
            self.settings.SongRequestAddedMessage
            .format(user_id, song_request)
        )
        self.logger.info(message)
        self.messenger.send_message(user_id, message)

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
        mod_ids = self.settings.parse_mod_ids(self.logger)
        self.messenger.send_message_for_group(mod_ids, message)

    def _handle_invalid_target(self, user_id, target):
        message = (
            self.settings.InvalidTargetMessage
            .format(user_id, target)
        )
        self.logger.info(message)
        self.messenger.send_message(user_id, message)

    def _handle_no_requests(self, user_id, target):
        message = (
            self.settings.NoSongRequestsMessage
            .format(user_id, target)
        )
        self.logger.info(message)
        self.messenger.send_message(user_id, message)

    def _handle_nonexistent_request_number(self, user_id, target_name,
                                           invalid_number):
        message = (
            self.settings.NonExistentSongRequestNumberMessage
            .format(user_id, invalid_number, target_name)
        )
        self.logger.info(message)
        self.messenger.send_message(user_id, message)

    def _format_with_reason(self, message, reason):
        if reason:
            text_reason = (
                self.settings.SongRequestDecisionReasonMessage.format(reason)
            )
            return "{0} {1}".format(message, text_reason)

        return message

    def _handle_request_approved(self, user_name, target_id, song_request,
                                 reason):
        message = (
            self.settings.SongRequestApprovedMessage
            .format(target_id, song_request, user_name)
        )
        message = self._format_with_reason(message, reason)

        self.logger.info(message)
        self.messenger.send_message(target_id, message)

    def _handle_request_rejected(self, user_name, target_id, song_request,
                                 reason):
        message = (
            self.settings.SongRequestRejectedMessage
            .format(target_id, song_request, user_name)
        )
        message = self._format_with_reason(message, reason)

        self.logger.info(message)
        self.messenger.send_message(target_id, message)


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
            seems_like_request_number.lower() == SongRequestNumber.RawAllValue.lower()
        )
        if param_count > 2:
            start_reason = 2 if not is_request_number else 3
            for i in range(start_reason, param_count):
                reason += " " + data_wrapper.get_param(i)
            reason = reason.strip()
        elif not is_request_number:
            reason = seems_like_request_number

    request_decision = SongRequestDecision(
        user_data, target_user_id_or_name, request_number, reason
    )

    if command == settings.CommandApproveSongRequest:
        manager.approve_request(request_decision)
    elif command == settings.CommandRejectSongRequest:
        manager.reject_request(request_decision)
    else:
        raise ValueError("Unexpected command to handle: {0}.".format(command))


def get_all_user_requests(data_wrapper, settings, logger, manager):
    user_data = helpers.wrap_user_data(
        data_wrapper.user_id, data_wrapper.user_name
    )

    raw_target_user_id_or_name = data_wrapper.get_param(1)
    target_user_id_or_name = helpers.wrap_user_id_or_name(
        raw_target_user_id_or_name
    )

    user_requests = manager.get_user_requests_for(
        user_data, target_user_id_or_name
    )

    message = None
    if user_requests:
        map_lambda = lambda request: format_song_request(
            request.SongLink.Value, request.RequestNumber.Value
        )
        processed_requests = map(map_lambda, user_requests)
        formatted_requests = " ".join(processed_requests)

        message = (
            settings.GotUserSongRequestsMessage
            .format(
                target_user_id_or_name.Value,
                len(user_requests),
                formatted_requests
            )
        )
    else:
        message = (
            settings.NoUserSongRequestsMessage
            .format(target_user_id_or_name.Value)
        )

    logger.info(message)
    manager.get_messenger().send_message(user_data.Id.Value, message)

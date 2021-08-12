# -*- coding: utf-8 -*-

from song_request_storage import SongRequestStorage as Storage
from song_request_user_searcher import SongRequestUserSearcher as UserSearcher

from song_request_dispatchers import PendingSongRequestDispatcher
from song_request_dispatchers import DeniedSongRequestDispatcher

from Scripts.SongRequest.CSharp.Models.Requests import SongRequestNumber
from Scripts.SongRequest.CSharp.Models.Requests import SongRequestModel


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

        user_requests = self.storage.get_user_requests(user_data.Id)
        number_of_requests = len(user_requests)
        if number_of_requests >= self.settings.MaxNumberOfSongRequestsToAdd:
            self._handle_limit_exceeded(user_data.Name.Value)
            return False

        number = SongRequestNumber(number_of_requests)
        request = SongRequestModel.CreateNew(user_data, song_link, number)
        self.storage.add_request(request)

        self._handle_request_added(user_data.Name.Value, song_link.Value)
        self._handle_request_to_approve(user_data.Name.Value, song_link.Value)
        return True

    def cancel_request(self):
        return

    def approve_request(self, request_decision):
        self.logger.debug(
            "Approving request with decision [{0}]."
            .format(request_decision)
        )

        target_data = self._prepare_target_data(request_decision)
        if not target_data.HasValue:
            self.logger.debug(
                "Target user {0} is invalid, interupt song request processing."
                .format(request_decision.TargetUserIdOrName.Value)
            )
            return False

        target_user_requests = self.storage.get_user_requests(target_data.Id)
        if not target_user_requests:
            self._handle_no_requests(
                request_decision.UserData.Name.Value,
                request_decision.TargetUserIdOrName.Value
            )
            return False

        target_user_requests_to_use = target_user_requests
        if not request_decision.RequestNumber.IsAll:
            if len(target_user_requests) < request_decision.RequestNumber.Value:
                self._handle_nonexistent_request_number(
                    request_decision.UserData.Name.Value,
                    request_decision.TargetUserIdOrName.Value,
                    request_decision.RequestNumber.Value
                )
                return False

            index_to_use = request_decision.RequestNumber.Value - 1
            target_user_requests_to_use = [target_user_requests[index_to_use]]

        for i in range(len(target_user_requests_to_use)):
            request = target_user_requests_to_use[i]
            if request.IsWaitingForApproval:
                target_user_requests_to_use[i] = request.Approve()
                self._handle_request_approved(
                    request_decision.UserData.Name.Value,
                    request_decision.TargetUserIdOrName.Value,
                    request.SongLink.Value
                )

        self.storage.update_states(target_user_requests_to_use)
        return True

    def reject_request(self):
        return

    def request_processed(self, is_success):
        return

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
            .format(song_request, user_name)
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

    def _handle_request_approved(self, user_name, target, song_request):
        message = (
            self.settings.SongRequestApprovedMessage
            .format(target, song_request, user_name)
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)


def create_manager(parent_wrapper, settings, logger, page_scrapper):
    dispatchers = [
        PendingSongRequestDispatcher(parent_wrapper, settings, logger, page_scrapper),
        DeniedSongRequestDispatcher(parent_wrapper, settings, logger)
    ]
    manager = SongRequestManager(parent_wrapper, settings, logger, dispatchers)
    return manager

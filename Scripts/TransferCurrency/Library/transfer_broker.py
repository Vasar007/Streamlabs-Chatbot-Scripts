# -*- coding: utf-8 -*-

import transfer_helpers as helpers
from transfer_searcher import TransferUserSearcher as UserSearcher


class TransferRequest(object):

    def __init__(self, user_id, user_name, target, currency_name, amount):
        self.user_id = user_id
        self.user_name = user_name
        self.target = target
        self.currency_name = currency_name
        self.amount = amount


class TransferBroker(object):

    def __init__(self, parent_wrapper, settings, logger):
        self.parent_wrapper = parent_wrapper
        self.settings = settings
        self.logger = logger
        self.searcher = UserSearcher(parent_wrapper, logger)

    def try_send_transfer(self, request):
        target_id_and_name = self.searcher.find_user_id_and_name(
            request.target
        )
        if target_id_and_name is None:
            if not request.target:
                self._handle_no_target(
                    request.user_name, request.currency_name
                )
            else:
                self._handle_invalid_target(request.user_name, request.target)
            return

        target_id, target_name = target_id_and_name
        if request.user_id == target_id:
            self._handle_target_is_sender(
                request.user_name, request.currency_name
            )
            return

        amount_int = helpers.safe_cast(request.amount, int)
        if amount_int is None or amount_int <= 0:
            self._handle_invalid_amount(request.user_name, request.amount)
        elif amount_int <= self.parent_wrapper.get_points(request.user_id):
            self._handle_transfer_currency(
                request, target_id, target_name, amount_int
            )
        else:
            self._handle_not_enough_funds(
                request.user_name, request.currency_name
            )

    def _handle_invalid_amount(self, user_name, amount):
        message = (
            str(self.settings.InvalidAmountMessage)
            .format(user_name, amount)
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def _handle_transfer_currency(self, request, target_id, target_name,
                                  amount_int):
        user_id = request.user_id
        user_name = request.user_name
        currency_name = request.currency_name

        current_user_points = self.parent_wrapper.get_points(request.user_id)
        current_target_points = self.parent_wrapper.get_points(target_id)
        self.logger.debug(
            "User {0} has {1} {2} before transfer"
            .format(user_id, current_user_points, currency_name)
        )
        self.logger.debug(
            "User {0} has {1} {2} before transfer"
            .format(target_id, current_target_points, currency_name)
        )

        self.parent_wrapper.remove_points(user_id, amount_int)
        self.parent_wrapper.add_points(target_id, amount_int)
        message = (
            str(self.settings.SuccessfulTransferMessage)
            .format(user_name, amount_int, currency_name, target_name)
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

        current_user_points = self.parent_wrapper.get_points(user_id)
        current_target_points = self.parent_wrapper.get_points(target_id)
        self.logger.debug(
            "User {0} has {1} {2} after transfer"
            .format(user_id, current_user_points, currency_name)
        )
        self.logger.debug(
            "User {0} has {1} {2} after transfer"
            .format(target_id, current_target_points, currency_name)
        )

    def _handle_not_enough_funds(self, user_name, currency_name):
        message = (
            str(self.settings.NotEnoughFundsMessage)
            .format(user_name, currency_name)
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def _handle_no_target(self, user_name, currency_name):
        message = (
            str(self.settings.NoTargetMessage)
            .format(user_name, currency_name)
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def _handle_invalid_target(self, user_name, target):
        message = (
            str(self.settings.InvalidTargetMessage)
            .format(user_name, target)
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def _handle_target_is_sender(self, user_name, currency_name):
        message = (
            str(self.settings.TransferToYourselfMessage)
            .format(user_name, currency_name)
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)


def create_request_from(data, parent_wrapper):
    user_id = data.User
    user_name = data.UserName
    target = data.GetParam(1)
    amount = data.GetParam(2)
    currency_name = parent_wrapper.get_currency_name()
    return TransferRequest(user_id, user_name, target, currency_name, amount)


def handle_request(request, parent_wrapper, settings, logger):
    broker = TransferBroker(parent_wrapper, settings, logger)
    broker.try_send_transfer(request)

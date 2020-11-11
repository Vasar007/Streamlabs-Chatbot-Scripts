# -*- coding: utf-8 -*-

import transfer_config as config  # pylint:disable=import-error
import transfer_helpers as helpers

from transfer_searcher import TransferUserSearcher as UserSearcher
from transfer_tax_collector import TransferTaxCollector as TaxCollector
from transfer_user_data import TransferUserData as UserData

from transfer_broker_models import TransferType
from transfer_broker_models import TransferParameters
from transfer_broker_models import TransferRequest
from transfer_broker_models import TransferValidationIssueType as IssueType

import transfer_broker_strategies as strategies


class TransferBroker(object):

    def __init__(self, parent_wrapper, settings, logger):
        self.parent_wrapper = parent_wrapper
        self.settings = settings
        self.logger = logger

        self.searcher = UserSearcher(parent_wrapper, logger)
        self.tax_collector = TaxCollector(parent_wrapper, settings, logger)

    def try_send_transfer(self, request):
        target_data = self._prepare_transfer(request)
        if target_data.is_empty():
            self.logger.debug("Target is invalid, interupt tranfer.")
            return False

        strategy = self._create_transfer_strategy(request.transfer_type)

        validation_result = strategy.validate_transfer(
            request.user_data.id, target_data.id
        )
        if not validation_result.is_valid:
            self._handle_invalid_validation(
                validation_result.issue_type,
                request.user_data,
                target_data.name,
                request.currency_name
            )
            return False

        amount_int = strategy.try_get_amount_value(
            request.user_data.id, target_data.id, request.raw_amount
        )
        is_amount_invalid = (
            amount_int is None or
            not strategy.check_amount_value(amount_int)
        )
        if is_amount_invalid:
            strategy.handle_invalid_amount(
                request.user_data.name, request.raw_amount
            )
            return False

        self.logger.info("Initial amount to transfer: {0}.".format(amount_int))
        final_amount = strategy.calculate_final_amount(
            request.user_data.id, amount_int
        )
        has_enough_funds = strategy.has_enough_funds(
            request.user_data.id, target_data.id, final_amount
        )
        if not has_enough_funds:
            strategy.handle_not_enough_funds(
                request.user_data,
                target_data,
                request.currency_name,
                final_amount
            )
            return False

        strategy.handle_transfer_request(request, target_data, final_amount)
        return True

    def _prepare_transfer(self, request):
        # Retrive data about target.
        target_data = self.searcher.find_user_data(
            request.target_id_or_name
        )
        if target_data.is_empty():
            if not request.target_id_or_name:
                self._handle_no_target(
                    request.user_data.name, request.currency_name
                )
            else:
                self._handle_invalid_target(
                    request.user_data.name, request.target_id_or_name
                )
            # "target_data" == UserData.empty() here.
            return target_data

        return target_data

    def _create_transfer_strategy(self, transfer_type):
        # Normal transfer case.
        if transfer_type == TransferType.NormalTransfer:
            return strategies.NormalTransferStrategy(
                self.parent_wrapper, self.settings, self.logger,
                self.tax_collector
            )

        # Add transfer case.
        elif transfer_type == TransferType.AddTransfer:
            return strategies.AddTransferStrategy(
                self.parent_wrapper, self.settings, self.logger
            )

        # Remove transfer case.
        elif transfer_type == TransferType.RemoveTransfer:
            return strategies.RemoveTransferStrategy(
                self.parent_wrapper, self.settings, self.logger
            )

        # Set transfer case.
        elif transfer_type == TransferType.SetTransfer:
            return strategies.SetTransferStrategy(
                self.parent_wrapper, self.settings, self.logger
            )

        # Default case.
        else:
            raise ValueError(
                "Unexpected transfer request type to handle: {0}."
                .format(transfer_type)
            )

    def _handle_no_target(self, user_name, currency_name):
        message = (
            self.settings.NoTargetMessage
            .format(user_name, currency_name)
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

    def _handle_invalid_validation(self, issue_type, user_name, target_name,
                                   currency_name):
        # Denied transfer to youself case.
        if issue_type == IssueType.DeniedTransferToYouself:
            self._handle_target_is_sender(user_name, currency_name)

        # Denied operation case.
        elif issue_type == IssueType.DeniedOperation:
            self._handle_operation_denied(target_name, currency_name)

        # Default case.
        else:
            raise ValueError(
                "Unexpected validation request type to handle: {0}."
                .format(issue_type)
            )

    def _handle_target_is_sender(self, user_name, currency_name):
        message = (
            self.settings.DeniedTransferToYourselfMessage
            .format(user_name, currency_name)
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def _handle_operation_denied(self, target_name, currency_name):
        message = (
            self.settings.OperationDeniedMessage
            .format(target_name, currency_name)
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)


def get_transfer_type(command, settings):
    if command == settings.CommandGive:
        return TransferType.NormalTransfer
    elif command == settings.CommandAdd:
        return TransferType.AddTransfer
    elif command == settings.CommandRemove:
        return TransferType.RemoveTransfer
    elif command == settings.CommandSet:
        return TransferType.SetTransfer
    else:
        raise ValueError(
            "Unexpected command to get transfer type: {0}.".format(command)
        )


def create_request_from(data_wrapper, command, parent_wrapper, settings):
    user_data = UserData(data_wrapper.user_id, data_wrapper.user_name)

    raw_target_id_or_name = data_wrapper.get_param(1)
    target_id_or_name = helpers.strip_at_symbol_for_name(raw_target_id_or_name)

    raw_amount = data_wrapper.get_param(2).lower()
    currency_name = parent_wrapper.get_currency_name()
    transfer_type = get_transfer_type(command, settings)

    return TransferRequest(
        user_data, target_id_or_name, currency_name, raw_amount, transfer_type
    )


def handle_request(request, parent_wrapper, settings, logger):
    broker = TransferBroker(parent_wrapper, settings, logger)
    broker.try_send_transfer(request)

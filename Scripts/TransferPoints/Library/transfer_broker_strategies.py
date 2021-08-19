# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

import transfer_config as config
import transfer_helpers as helpers

from transfer_broker_models import TransferAmount
from transfer_broker_models import TransferValidationIssueType as IssueType
from transfer_broker_models import TransferValidationResult

from transfer_permissions import TransferPermissionHandler as PermissionHandler
from transfer_permissions import TransferPermissionChecker as PermissionChecker

from transfer_transaction import TransferTransaction


class BaseTransferStrategy(object):

    __metaclass__ = ABCMeta

    def __init__(self, parent_wrapper, settings, logger):
        self._parent_wrapper = parent_wrapper
        self._settings = settings
        self._logger = logger

    @abstractmethod
    def validate_transfer(self, user_id, target_id):
        raise NotImplementedError()

    @abstractmethod
    def try_get_amount_value(self, user_id, target_id, raw_amount):
        raise NotImplementedError()

    @abstractmethod
    def check_amount_value(self, amount):
        raise NotImplementedError()

    @abstractmethod
    def handle_invalid_amount(self, user_name, raw_amount):
        raise NotImplementedError()

    @abstractmethod
    def calculate_final_amount(self, user_id, amount):
        raise NotImplementedError()

    @abstractmethod
    def has_enough_funds(self, user_id, target_id, transfer_amount):
        raise NotImplementedError()

    @abstractmethod
    def handle_not_enough_funds(self, user_data, target_data, currency_name,
                                transfer_amount):
        raise NotImplementedError()

    @abstractmethod
    def handle_transfer_request(self, request, target_data, transfer_amount):
        raise NotImplementedError()

    def _can_transfer_to_youself(self, user_id, target_id):
        """
        Checks whether transfer to youself is allowed.
        """
        return (
            self._settings.AllowToTransferToYourself or
            user_id != target_id
        )

    def _is_operation_allowed(self, user_id, target_id, permission_handler):
        """
        Checks whether target user has enough permission to deny operation.

        Contract: check of caller user permission should be applied before this
        method call.
        """
        if self._settings.AllowToAddRemoveSetForOtherWithSamePermissionOrHigher:
            return True

        # Retrieve target user permission. If target has required permission,
        # operation should be denied. It can prevent moderator from changing
        # own points and other moderator's points, for example.

        checker = PermissionChecker(self._parent_wrapper, self._logger)
        check_result = checker.check_permissions(
            user_id, target_id, permission_handler
        )
        # Should return true only when user has higher permission.
        # user > target == -1
        return check_result < 0

    def _validate_transfer(self, user_id, target_id, permission_handler=None):
        if not self._can_transfer_to_youself(user_id, target_id):
            return TransferValidationResult.failed(
                IssueType.DeniedTransferToYouself
            )

        is_operation_allowed = (
            permission_handler is None or
            self._is_operation_allowed(user_id, target_id, permission_handler)
        )
        if not is_operation_allowed:
            return TransferValidationResult.failed(IssueType.DeniedOperation)

        return TransferValidationResult.successful()

    def _handle_add_tranfer(self, parameters, send_message):
        user_name = parameters.user_data.name
        target_id = parameters.target_data.id
        target_name = parameters.target_data.name
        final_amount = parameters.final_amount
        currency_name = parameters.currency_name

        self._log_current_currency(target_id, currency_name, "before adding")

        is_success = self._parent_wrapper.add_points(target_id, final_amount)
        self._logger.debug(
            "Add points completed with status: " + str(is_success)
        )
        if send_message:
            message = (
                self._settings.SuccessfulAddingMessage
                .format(user_name, final_amount, currency_name, target_name)
            )
            self._logger.info(message)
            self._parent_wrapper.send_stream_message(message)

        self._log_current_currency(target_id, currency_name, "after adding")
        return is_success

    def _handle_remove_tranfer(self, parameters, send_message):
        user_name = parameters.user_data.name
        target_id = parameters.target_data.id
        target_name = parameters.target_data.name
        final_amount = parameters.final_amount
        currency_name = parameters.currency_name

        self._log_current_currency(target_id, currency_name, "before removing")

        is_success = self._parent_wrapper.remove_points(target_id, final_amount)
        self._logger.debug(
            "Remove points completed with status: " + str(is_success)
        )
        if send_message:
            message = (
                self._settings.SuccessfulRemovingMessage
                .format(user_name, final_amount, currency_name, target_name)
            )
            self._logger.info(message)
            self._parent_wrapper.send_stream_message(message)

        self._log_current_currency(target_id, currency_name, "after removing")
        return is_success

    def _log_current_currency(self, user_id, currency_name, message_part):
        current_points = self._parent_wrapper.get_points(user_id)
        self._logger.debug(
            "User {0} has {1} {2} {3}."
            .format(user_id, current_points, currency_name, message_part)
        )

    def _create_transaction(self):
        return TransferTransaction(
            self._logger,
            self._handle_add_tranfer,
            self._handle_remove_tranfer
        )

    def _is_all_parameter(self, raw_amount):
        return self._settings.is_all_parameter(raw_amount)


class NormalTransferStrategy(BaseTransferStrategy):

    def __init__(self, parent_wrapper, settings, logger, tax_collector):
        super(NormalTransferStrategy, self).__init__(
            parent_wrapper, settings, logger
        )

        self._tax_collector = tax_collector

    def validate_transfer(self, user_id, target_id):
        return self._validate_transfer(user_id, target_id)

    def try_get_amount_value(self, user_id, target_id, raw_amount):
        if self._is_all_parameter(raw_amount):
            return self._parent_wrapper.get_points(user_id)

        return helpers.safe_cast(raw_amount, int)

    def check_amount_value(self, amount):
        min_amount = self._settings.MinGiveAmount
        max_amount = self._settings.MaxGiveAmount

        if max_amount < min_amount:
            min_amount = config.MinGiveAmount
            max_amount = config.MaxGiveAmount
            self._logger.error(
                "Encountered invalid amount settings. " +
                "Using default value for min ({0}) and max ({1}) amount."
                .format(min_amount, max_amount)
            )

        return min_amount <= amount <= max_amount

    def handle_invalid_amount(self, user_name, raw_amount):
        amount_example = config.ExampleAmountMinMaxRange.format(
            self._settings.MinGiveAmount, self._settings.MaxGiveAmount
        )

        message = (
            self._settings.InvalidAmountMessage
            .format(user_name, raw_amount, amount_example)
        )
        self._logger.info(message)
        self._parent_wrapper.send_stream_message(message)

    def calculate_final_amount(self, user_id, amount):
        (final_amount, fee) = self._tax_collector.apply_fee(
            user_id, amount, return_fee=True
        )
        return TransferAmount(amount, final_amount, fee)

    def has_enough_funds(self, user_id, target_id, transfer_amount):
        current_amount = self._parent_wrapper.get_points(user_id)
        return transfer_amount.initial_amount <= current_amount

    def handle_not_enough_funds(self, user_data, target_data, currency_name,
                                transfer_amount):
        current_amount = self._parent_wrapper.get_points(user_data.id)
        message = (
            self._settings.NotEnoughFundsToTransferMessage
            .format(
                user_data.name,
                currency_name,
                current_amount,
                transfer_amount.initial_amount
            )
        )
        self._logger.info(message)
        self._parent_wrapper.send_stream_message(message)

    def handle_transfer_request(self, request, target_data, transfer_amount):
        self._handle_normal_transfer(request, target_data, transfer_amount)

    def _handle_normal_transfer(self, request, target_data, transfer_amount):
        # Normal transfer is implemented as two function call:
        # 1. Remove specified points from the caller user.
        # 2. Add specified number of points to the target user.
        with self._create_transaction() as transaction:
            # Remove points from the caller user.
            remove_parameters = request.to_paramters(
                target_data=request.user_data,
                final_amount=transfer_amount.initial_amount
            )
            transaction.execute_remove(remove_parameters, send_message=False)

            # Add points to the target user.
            add_parameters = request.to_paramters(
                target_data=target_data,
                final_amount=transfer_amount.final_amount
            )
            transaction.execute_add(add_parameters, send_message=False)

            # Send message to chat.
            message = (
                self._settings.SuccessfulTransferMessage
                .format(
                    request.user_data.name,
                    transfer_amount.final_amount,
                    request.currency_name,
                    target_data.name,
                    transfer_amount.fee
                )
            )
            self._parent_wrapper.send_stream_message(message)

            # Commit changes.
            transaction.commit()


class AddTransferStrategy(BaseTransferStrategy):

    def __init__(self, parent_wrapper, settings, logger):
        super(AddTransferStrategy, self).__init__(
            parent_wrapper, settings, logger
        )

    def validate_transfer(self, user_id, target_id):
        permission = self._settings.PermissionOnAddRemoveSet
        permission_info = self._settings.PermissionInfoOnAddRemoveSet
        permission_handler = PermissionHandler(permission, permission_info)
        return self._validate_transfer(user_id, target_id, permission_handler)

    def try_get_amount_value(self, user_id, target_id, raw_amount):
        return helpers.safe_cast(raw_amount, int)

    def check_amount_value(self, amount):
        return amount > 0

    def handle_invalid_amount(self, user_name, raw_amount):
        message = (
            self._settings.InvalidAmountMessage
            .format(user_name, raw_amount, config.ExampleAmountValidRange)
        )
        self._logger.info(message)
        self._parent_wrapper.send_stream_message(message)

    def calculate_final_amount(self, user_id, amount):
        return TransferAmount(amount, amount)

    def has_enough_funds(self, user_id, target_id, transfer_amount):
        return True

    def handle_not_enough_funds(self, user_data, target_data, currency_name,
                                transfer_amount):
        # Nothing to do. This method should never be called for this class.
        raise NotImplementedError()

    def handle_transfer_request(self, request, target_data, transfer_amount):
        with self._create_transaction() as transaction:
            # Add points to the target user.
            add_parameters = request.to_paramters(
                target_data=target_data,
                final_amount=transfer_amount.final_amount
            )
            transaction.execute_add(add_parameters, send_message=True)

            # Commit changes.
            transaction.commit()


class RemoveTransferStrategy(BaseTransferStrategy):

    def __init__(self, parent_wrapper, settings, logger):
        super(RemoveTransferStrategy, self).__init__(
            parent_wrapper, settings, logger
        )

    def validate_transfer(self, user_id, target_id):
        permission = self._settings.PermissionOnAddRemoveSet
        permission_info = self._settings.PermissionInfoOnAddRemoveSet
        permission_handler = PermissionHandler(permission, permission_info)
        return self._validate_transfer(user_id, target_id, permission_handler)

    def try_get_amount_value(self, user_id, target_id, raw_amount):
        if self._is_all_parameter(raw_amount):
            return self._parent_wrapper.get_points(target_id)

        return helpers.safe_cast(raw_amount, int)

    def check_amount_value(self, amount):
        return amount > 0

    def handle_invalid_amount(self, user_name, raw_amount):
        message = (
            self._settings.InvalidAmountMessage
            .format(user_name, raw_amount, config.ExampleAmountValidRange)
        )
        self._logger.info(message)
        self._parent_wrapper.send_stream_message(message)

    def calculate_final_amount(self, user_id, amount):
        return TransferAmount(amount, amount)

    def has_enough_funds(self, user_id, target_id, transfer_amount):
        current_amount = self._parent_wrapper.get_points(target_id)
        return transfer_amount.final_amount <= current_amount

    def handle_not_enough_funds(self, user_data, target_data, currency_name,
                                transfer_amount):
        current_amount = self._parent_wrapper.get_points(target_data.id)
        message = (
            self._settings.NotEnoughFundsToRemoveMessage
            .format(
                user_data.name,
                target_data.name,
                currency_name,
                current_amount,
                transfer_amount.final_amount
            )
        )
        self._logger.info(message)
        self._parent_wrapper.send_stream_message(message)

    def handle_transfer_request(self, request, target_data, transfer_amount):
        with self._create_transaction() as transaction:
            # Remove points from the target user.
            remove_parameters = request.to_paramters(
                target_data=target_data,
                final_amount=transfer_amount.final_amount
            )
            transaction.execute_remove(remove_parameters, send_message=True)

            # Commit changes.
            transaction.commit()


class SetTransferStrategy(BaseTransferStrategy):

    def __init__(self, parent_wrapper, settings, logger):
        super(SetTransferStrategy, self).__init__(
            parent_wrapper, settings, logger
        )

    def validate_transfer(self, user_id, target_id):
        permission = self._settings.PermissionOnAddRemoveSet
        permission_info = self._settings.PermissionInfoOnAddRemoveSet
        permission_handler = PermissionHandler(permission, permission_info)
        return self._validate_transfer(user_id, target_id, permission_handler)

    def try_get_amount_value(self, user_id, target_id, raw_amount):
        return helpers.safe_cast(raw_amount, int)

    def check_amount_value(self, amount):
        return amount >= 0

    def handle_invalid_amount(self, user_name, raw_amount):
        message = (
            self._settings.InvalidAmountMessage
            .format(user_name, raw_amount, config.ExampleAmountSetRange)
        )
        self._logger.info(message)
        self._parent_wrapper.send_stream_message(message)

    def calculate_final_amount(self, user_id, amount):
        return TransferAmount(amount, amount)

    def has_enough_funds(self, user_id, target_id, transfer_amount):
        return True

    def handle_not_enough_funds(self, user_data, target_data, currency_name,
                                transfer_amount):
        # Nothing to do. This method should never be called for this class.
        raise NotImplementedError()

    def handle_transfer_request(self, request, target_data, transfer_amount):
        self._handle_set_transfer(request, target_data, transfer_amount)

    def _handle_set_transfer(self, request, target_data, transfer_amount):
        # Set transfer is implemented as two function call:
        # 1. Remove all points from the target user.
        # 2. Add specified number of points to the target user.
        with self._create_transaction() as transaction:
            # Remove points from the target user.
            current_amount = self._parent_wrapper.get_points(target_data.id)
            remove_parameters = request.to_paramters(
                target_data=target_data,
                final_amount=current_amount
            )
            transaction.execute_remove(remove_parameters, send_message=False)

            # Add points to the target user.
            add_parameters = request.to_paramters(
                target_data=target_data,
                final_amount=transfer_amount.final_amount
            )
            transaction.execute_add(add_parameters, send_message=False)

            # Send message to chat.
            message = (
                self._settings.SuccessfulSettingMessage
                .format(
                    request.user_data.name,
                    transfer_amount.final_amount,
                    request.currency_name,
                    target_data.name
                )
            )
            self._parent_wrapper.send_stream_message(message)

            # Commit changes.
            transaction.commit()

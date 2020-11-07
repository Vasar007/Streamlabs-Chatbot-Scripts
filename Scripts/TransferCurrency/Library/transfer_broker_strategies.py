# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

import transfer_config as config  # pylint:disable=import-error
import transfer_helpers as helpers


class BaseTransferStrategy(object):

    __metaclass__ = ABCMeta

    def __init__(self, parent_wrapper, settings, logger):
        self.parent_wrapper = parent_wrapper
        self.settings = settings
        self.logger = logger

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
    def has_user_enough_funds(self, user_id, target_id, final_amount):
        raise NotImplementedError()

    @abstractmethod
    def handle_not_enough_funds(self, user_name, target_name, currency_name):
        raise NotImplementedError()

    @abstractmethod
    def handle_transfer_request(self, request, target_data, final_amount):
        raise NotImplementedError()

    def _handle_add_tranfer(self, parameters, send_message):
        user_name = parameters.user_data.name
        target_id = parameters.target_data.id
        target_name = parameters.target_data.name
        final_amount = parameters.final_amount
        currency_name = parameters.currency_name

        self._log_current_currency(target_id, currency_name, "before adding")

        self.parent_wrapper.add_points(target_id, final_amount)
        if send_message:
            message = (
                str(self.settings.SuccessfulAddingMessage)
                .format(user_name, final_amount, currency_name, target_name)
            )
            self.logger.info(message)
            self.parent_wrapper.send_stream_message(message)

        self._log_current_currency(target_id, currency_name, "after adding")

    def _handle_remove_tranfer(self, parameters, send_message):
        user_name = parameters.user_data.name
        target_id = parameters.target_data.id
        target_name = parameters.target_data.name
        final_amount = parameters.final_amount
        currency_name = parameters.currency_name

        self._log_current_currency(target_id, currency_name, "before removing")

        self.parent_wrapper.remove_points(target_id, final_amount)
        if send_message:
            message = (
                str(self.settings.SuccessfulRemovingMessage)
                .format(user_name, final_amount, currency_name, target_name)
            )
            self.logger.info(message)
            self.parent_wrapper.send_stream_message(message)

        self._log_current_currency(target_id, currency_name, "after removing")

    def _log_current_currency(self, user_id, currency_name, message_part):
        current_points = self.parent_wrapper.get_points(user_id)
        self.logger.debug(
            "User {0} has {1} {2} {3}."
            .format(user_id, current_points, currency_name, message_part)
        )


class NormalTransferStrategy(BaseTransferStrategy):

    def __init__(self, parent_wrapper, settings, logger, tax_collector):
        super(NormalTransferStrategy, self).__init__(
            parent_wrapper, settings, logger
        )

        self.tax_collector = tax_collector

    def try_get_amount_value(self, user_id, target_id, raw_amount):
        if raw_amount == self.settings.ParameterAll:
            return self.parent_wrapper.get_points(user_id)

        return helpers.safe_cast(raw_amount, int)

    def check_amount_value(self, amount):
        min_amount = self.settings.MinGiveAmount
        max_amount = self.settings.MaxGiveAmount

        if max_amount < min_amount:
            min_amount = config.MinGiveAmount
            max_amount = config.MaxGiveAmount
            self.logger.error(
                "Encountered invalid amount settings. " +
                "Using default value for min ({0}) and max ({1}) amount."
                .format(min_amount, max_amount)
            )

        return min_amount <= amount <= max_amount

    def handle_invalid_amount(self, user_name, raw_amount):
        amount_example = config.ExampleAmountMinMaxRange.format(
            self.settings.MinGiveAmount, self.settings.MaxGiveAmount
        )

        message = (
            str(self.settings.InvalidAmountMessage)
            .format(
                user_name, raw_amount, amount_example
            )
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def calculate_final_amount(self, user_id, amount):
        return self.tax_collector.apply_fee(user_id, amount)

    def has_user_enough_funds(self, user_id, target_id, final_amount):
        current_amount = self.parent_wrapper.get_points(user_id)
        return final_amount <= current_amount

    def handle_not_enough_funds(self, user_name, target_name, currency_name):
        message = (
            str(self.settings.NotEnoughFundsToTransferMessage)
            .format(user_name, currency_name)
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def handle_transfer_request(self, request, target_data, final_amount):
        self._handle_normal_transfer(request, target_data, final_amount)

    def _handle_normal_transfer(self, request, target_data, final_amount):
        remove_parameters = request.to_paramters(
            target_data=request.user_data,
            final_amount=final_amount
        )
        self._handle_remove_tranfer(remove_parameters, send_message=False)

        add_parameters = request.to_paramters(
            target_data=target_data,
            final_amount=final_amount
        )
        self._handle_add_tranfer(add_parameters, send_message=False)

        message = (
            str(self.settings.SuccessfulTransferMessage)
            .format(
                request.user_data.name,
                final_amount,
                request.currency_name,
                target_data.name
            )
        )
        self.parent_wrapper.send_stream_message(message)


class AddTransferStrategy(BaseTransferStrategy):

    def __init__(self, parent_wrapper, settings, logger):
        super(AddTransferStrategy, self).__init__(
            parent_wrapper, settings, logger
        )

    def try_get_amount_value(self, user_id, target_id, raw_amount):
        return helpers.safe_cast(raw_amount, int)

    def check_amount_value(self, amount):
        return amount > 0

    def handle_invalid_amount(self, user_name, raw_amount):
        message = (
            str(self.settings.InvalidAmountMessage)
            .format(
                user_name, raw_amount, config.ExampleAmountValidRange
            )
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def calculate_final_amount(self, user_id, amount):
        return amount

    def has_user_enough_funds(self, user_id, target_id, final_amount):
        return True

    def handle_not_enough_funds(self, user_name, target_name, currency_name):
        # Nothing to do. This method should never be called for this class.
        raise NotImplementedError()

    def handle_transfer_request(self, request, target_data, final_amount):
        add_parameters = request.to_paramters(
            target_data=target_data,
            final_amount=final_amount
        )
        self._handle_add_tranfer(add_parameters, send_message=True)


class RemoveTransferStrategy(BaseTransferStrategy):

    def __init__(self, parent_wrapper, settings, logger):
        super(RemoveTransferStrategy, self).__init__(
            parent_wrapper, settings, logger
        )

    def try_get_amount_value(self, user_id, target_id, raw_amount):
        if raw_amount == self.settings.ParameterAll:
            return self.parent_wrapper.get_points(target_id)

        return helpers.safe_cast(raw_amount, int)

    def check_amount_value(self, amount):
        return amount > 0

    def handle_invalid_amount(self, user_name, raw_amount):
        message = (
            str(self.settings.InvalidAmountMessage)
            .format(
                user_name, raw_amount, config.ExampleAmountValidRange
            )
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def calculate_final_amount(self, user_id, amount):
        return amount

    def has_user_enough_funds(self, user_id, target_id, final_amount):
        current_amount = self.parent_wrapper.get_points(target_id)
        return final_amount <= current_amount

    def handle_not_enough_funds(self, user_name, target_name, currency_name):
        message = (
            str(self.settings.NotEnoughFundsToRemoveMessage)
            .format(user_name, target_name, currency_name)
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def handle_transfer_request(self, request, target_data, final_amount):
        remove_parameters = request.to_paramters(
            target_data=target_data,
            final_amount=final_amount
        )
        self._handle_remove_tranfer(remove_parameters, send_message=True)


class SetTransferStrategy(BaseTransferStrategy):

    def __init__(self, parent_wrapper, settings, logger):
        super(SetTransferStrategy, self).__init__(
            parent_wrapper, settings, logger
        )

    def try_get_amount_value(self, user_id, target_id, raw_amount):
        return helpers.safe_cast(raw_amount, int)

    def check_amount_value(self, amount):
        return amount >= 0

    def handle_invalid_amount(self, user_name, raw_amount):
        message = (
            str(self.settings.InvalidAmountMessage)
            .format(
                user_name, raw_amount, config.ExampleAmountSetRange
            )
        )
        self.logger.info(message)
        self.parent_wrapper.send_stream_message(message)

    def calculate_final_amount(self, user_id, amount):
        return amount

    def has_user_enough_funds(self, user_id, target_id, final_amount):
        return True

    def handle_not_enough_funds(self, user_name, target_name, currency_name):
        # Nothing to do. This method should never be called for this class.
        raise NotImplementedError()

    def handle_transfer_request(self, request, target_data, final_amount):
        current_amount = self.parent_wrapper.get_points(target_data.id)
        remove_parameters = request.to_paramters(
            target_data=target_data,
            final_amount=current_amount
        )
        self._handle_remove_tranfer(remove_parameters, send_message=False)

        add_parameters = request.to_paramters(
            target_data=target_data,
            final_amount=final_amount
        )
        self._handle_add_tranfer(add_parameters, send_message=False)

        message = (
            str(self.settings.SuccessfulSettingMessage)
            .format(
                request.user_data.name,
                final_amount,
                request.currency_name,
                target_data.name
            )
        )
        self.parent_wrapper.send_stream_message(message)

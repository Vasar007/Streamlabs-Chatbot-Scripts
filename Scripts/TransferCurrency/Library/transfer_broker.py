# -*- coding: utf-8 -*-

import transfer_helpers as helpers


class TransferBroker(object):

    def __init__(self, Parent, settings, logger):
        self.Parent = Parent
        self.settings = settings
        self.logger = logger

    def _log(self, message):
        self.logger.info(message)

    def try_send_transfer(self, userid, targetid, currency_name, amount):
        if targetid in self.Parent.GetViewerList():
            amount_int = helpers.safe_cast(amount, int)
            if amount_int is None or amount_int <= 0:
                self._handle_invalid_amount(userid, amount)
            elif amount_int <= self.Parent.GetPoints(userid):
                self._handle_transfer_currency(
                    userid, targetid, currency_name, amount_int
                )
            else:
                self._handle_not_enough_funds(userid, currency_name)
        else:
            if not targetid:
                self._handle_no_target(userid, currency_name)
            else:
                self._handle_no_target(userid, targetid)

    def _handle_invalid_amount(self, userid, amount):
        message = (
            str(self.settings.InvalidAmountMessage)
            .format(userid, amount)
        )
        self._log(message)
        self.Parent.SendTwitchMessage(message)

    def _handle_transfer_currency(self, userid, targetid, currency_name,
                                  amount_int):
        current_user_points = self.Parent.GetPoints(userid)
        current_target_points = self.Parent.GetPoints(targetid)
        self._log(
            "User {0} has {1} {2} before transfer"
            .format(userid, current_user_points, currency_name)
        )
        self._log(
            "User {0} has {1} {2} before transfer"
            .format(targetid, current_target_points, currency_name)
        )

        self.Parent.RemovePoints(userid, amount_int)
        self.Parent.AddPoints(targetid, amount_int)
        message = (
            str(self.settings.SuccessfulTransferMessage)
            .format(userid, amount_int, currency_name, targetid)
        )
        self._log(message)
        self.Parent.SendTwitchMessage(message)

        current_user_points = self.Parent.GetPoints(userid)
        current_target_points = self.Parent.GetPoints(targetid)
        self._log(
            "User {0} has {1} {2} after transfer"
            .format(userid, current_user_points, currency_name)
        )
        self._log(
            "User {0} has {1} {2} after transfer"
            .format(targetid, current_target_points, currency_name)
        )

    def _handle_not_enough_funds(self, userid, currency_name):
        message = (
            str(self.settings.NotEnoughFundsMessage)
            .format(userid, currency_name)
        )
        self._log(message)
        self.Parent.SendTwitchMessage(message)

    def _handle_no_target(self, userid, currency_name):
        message = (
            str(self.settings.NoTargetMessage)
            .format(userid, currency_name)
        )
        self._log(message)
        self.Parent.SendTwitchMessage(message)

    def _handle_invalid_target(self, userid, targetid):
        message = (
            str(self.settings.InvalidTargetMessage)
            .format(userid, targetid)
        )
        self._log(message)
        self.Parent.SendTwitchMessage(message)

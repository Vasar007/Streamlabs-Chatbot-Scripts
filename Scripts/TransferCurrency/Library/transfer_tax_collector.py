# -*- coding: utf-8 -*-

import math


class TransferTaxCollector(object):

    def __init__(self, parent_wrapper, settings, logger):
        self.parent_wrapper = parent_wrapper
        self.settings = settings
        self.logger = logger

    def calculate_fee(self, user_id, amount):
        percent = self._calculate_percent(user_id)
        # Round to the smallest integer >= raw fee.
        # Cast to int to remove points in formatting.
        fee = int(math.ceil(amount * percent))
        self.logger.info("Calculated fee: {0}".format(fee))
        return fee

    def apply_fee(self, user_id, amount, return_fee=False):
        fee = self.calculate_fee(user_id, amount)
        # Cast to int to remove points in formatting.
        final_amount = int(amount - fee)
        self.logger.info("Calculated final amount: {0}".format(final_amount))
        if return_fee:
            return (final_amount, fee)

        return final_amount

    def _calculate_percent(self, user_id):
        percent = self.settings.GiveTaxPercent
        if percent > 100:
            self.logger.debug("Tax percent is too large, set it to 100.")
            percent = 100

        self.logger.debug("Calculated tax percent: {0}".format(percent))
        return percent / 100.0

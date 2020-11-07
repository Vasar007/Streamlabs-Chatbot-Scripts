# -*- coding: utf-8 -*-


class TransferTaxCollector(object):

    def __init__(self, parent_wrapper, settings, logger):
        self.parent_wrapper = parent_wrapper
        self.settings = settings
        self.logger = logger

    def calculate_fee(self, user_id, amount):
        percent = self._calculate_percent(user_id)
        fee = int(amount * percent)
        self.logger.info("Calculated fee: {0}".format(fee))
        return fee

    def apply_fee(self, user_id, amount):
        fee = self.calculate_fee(user_id, amount)
        final_amount = amount - fee
        self.logger.info("Calculated final amount: {0}".format(final_amount))
        return final_amount

    def _calculate_percent(self, user_id):
        percent = self.settings.GiveTaxPercent
        if percent > 100:
            percent = 100
        self.logger.debug("Calculated tax percent: {0}".format(percent))
        return percent / 100.0

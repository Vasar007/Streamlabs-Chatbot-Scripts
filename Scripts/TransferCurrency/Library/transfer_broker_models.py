# -*- coding: utf-8 -*-


class TransferType:
    NormalTransfer = 1
    AddTransfer = 2
    RemoveTransfer = 3
    SetTransfer = 4


class TransferRequest(object):

    def __init__(self, user_data, target_id_or_name, currency_name, raw_amount,
                 transfer_type):
        self.user_data = user_data
        self.target_id_or_name = target_id_or_name
        self.currency_name = currency_name
        self.raw_amount = raw_amount
        self.transfer_type = transfer_type

    def to_paramters(self, target_data, final_amount):
        return TransferParameters(
            self.user_data, target_data, self.currency_name, final_amount
        )


class TransferParameters(object):

    def __init__(self, user_data, target_data, currency_name, final_amount):
        self.user_data = user_data
        self.target_data = target_data
        self.currency_name = currency_name
        self.final_amount = final_amount

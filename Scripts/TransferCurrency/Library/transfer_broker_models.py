# -*- coding: utf-8 -*-


class TransferType(object):
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


class TransferAmount(object):

    def __init__(self, initial_amount, final_amount, fee=0):
        self.initial_amount = initial_amount
        self.final_amount = final_amount
        self.fee = fee


class TransferValidationIssueType(object):
    DeniedTransferToYouself = 1
    DeniedOperation = 2


class TransferValidationResult(object):

    def __init__(self, is_valid, issue_type):
        self.is_valid = is_valid
        self.issue_type = issue_type

    @staticmethod
    def successful():
        return TransferValidationResult(True, None)

    @staticmethod
    def failed(issue_type):
        return TransferValidationResult(False, issue_type)

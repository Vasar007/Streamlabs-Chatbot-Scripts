# -*- coding: utf-8 -*-

import os
import codecs
import json

import transfer_config as config  # pylint:disable=import-error
import transfer_helpers as helpers


class TransferSettings(object):

    def __init__(self, Parent=None, settingsfile=None):
        """
        Load in saved settings file if available or else set default values.
        """
        if settingsfile is None:
            self._set_default()
        else:
            try:
                if os.path.isfile(settingsfile):
                    with codecs.open(settingsfile, encoding="utf-8-sig",
                                     mode="r") as f:
                        self.__dict__ = json.load(f, encoding="utf-8")
                else:
                    self._set_default()
            except Exception as ex:
                if Parent is not None:
                    helpers.log(Parent, "Failed to load setting: " + str(ex))
                self._set_default()

    def reload(self, jsondata):
        """
        Reload settings from Chatbot user interface by given json data.
        """
        self.__dict__ = json.loads(jsondata, encoding="utf-8")

    def save(self, settingsfile):
        """
        Save settings contained within to .json and .js settings files.
        """
        helpers.save_json(self.__dict__, settingsfile)

        with codecs.open(settingsfile.replace("json", "js"),
                         encoding="utf-8-sig", mode="w+") as f:
            content = (
                "var settings = {0};".format(
                    json.dumps(self.__dict__, encoding="utf-8")
                )
            )
            f.write(content)

    def _set_default(self):
        # Setup group.
        self.CommandGive = config.CommandGive

        # Permission group.
        self.Permission = config.Permission
        self.PermissionDeniedMessage = config.PermissionDeniedMessage
        self.PermissionInfo = config.PermissionInfo

        # Chat Messages group.
        self.SuccessfulTransferMessage = config.SuccessfulTransferMessage
        self.NotEnoughFundsMessage = config.NotEnoughFundsMessage
        self.InvalidAmountMessage = config.InvalidAmountMessage
        self.NoTargetMessage = config.NoTargetMessage
        self.InvalidTargetMessage = config.InvalidTargetMessage

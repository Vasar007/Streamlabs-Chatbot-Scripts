# -*- coding: utf-8 -*-

import os
import codecs
import json

import transfer_config as config  # pylint:disable=import-error
import transfer_helpers as helpers


class TransferSettings(object):

    _reload_callback = None

    def __init__(self, Parent=None, settingsfile=None):
        """
        Load in saved settings file if available or else set default values.
        """
        if settingsfile is None:
            self._set_default()
        else:
            try:
                if os.path.isfile(settingsfile):
                    with codecs.open(settingsfile, encoding="utf-8",
                                     mode="r") as f:
                        self.__dict__ = json.load(f, encoding="utf-8")
                else:
                    self._set_default()
            except Exception as ex:
                helpers.get_logger().exception(
                    "Failed to load setting: " + str(ex)
                )
                self._set_default()

    def reload(self, jsondata):
        """
        Reload settings from Chatbot user interface by given json data.
        """
        self.__dict__ = json.loads(jsondata, encoding="utf-8")

        if TransferSettings._reload_callback is not None:
            # pylint:disable=not-callable
            TransferSettings._reload_callback(self)

    def save(self, settingsfile):
        """
        Save settings contained within to .json and .js settings files.
        """
        helpers.save_json(self.__dict__, settingsfile)

        with codecs.open(settingsfile.replace("json", "js"),
                         encoding="utf-8", mode="w+") as f:
            content = (
                "var settings = {0};".format(
                    json.dumps(self.__dict__, encoding="utf-8")
                )
            )
            f.write(content)

    @classmethod
    def set_reload_callback(cls, reload_callback):
        """
        Allows to set callback on settings reload event.
        Callback should accept single parameter — current settings class.
        """
        cls._reload_callback = reload_callback

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

        # Debugging group.
        self.LoggingLevel = config.LoggingLevel

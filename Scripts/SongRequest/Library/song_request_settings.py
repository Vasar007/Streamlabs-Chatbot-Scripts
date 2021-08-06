# -*- coding: utf-8 -*-

import os
import codecs
import json

import song_request_config as config  # pylint:disable=import-error
import song_request_helpers as helpers
from song_request_event_emitter import SongRequestEventEmitter as EventEmitter 


class SongRequestSettings(object):

    _reload_event = EventEmitter()

    def __init__(self, settingsfile=None):
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

        SongRequestSettings._reload_event.emit(
            config.SettingsReloadEventName, self
        )

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
    def subscribe_on_reload(cls, reload_callback):
        """
        Allows to add callback on settings reload event.
        Callback should accept single parameter — current settings class.
        """
        cls._reload_event.on(config.SettingsReloadEventName, reload_callback)

    def _set_default(self):
        # Setup group.
        self.CommandPing = config.CommandPing
        self.Cooldown = config.Cooldown

        # Permission group.
        self.Permission = config.Permission
        self.PermissionDeniedMessage = config.PermissionDeniedMessage
        self.PermissionInfo = config.PermissionInfo

        # Chat Messages group.
        self.InvalidCommandCallMessage = config.InvalidCommandCallMessage
        self.ResponseMessage = config.ResponseMessage

        # Debugging group.
        self.LoggingLevel = config.LoggingLevel
        self.AllowLoggingToFile = config.AllowLoggingToFile

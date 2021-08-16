# -*- coding: utf-8 -*-

import os
import codecs
import json

import score_config as config
import score_helpers as helpers
from score_event_emitter import ScoreEventEmitter as EventEmitter 


class ScoreSettings(object):

    _reload_event = EventEmitter()

    def __init__(self, settingsfile=None, encoding="utf-8"):
        """
        Load in saved settings file if available or else set default values.
        """
        if settingsfile is None:
            self._set_default()
        else:
            try:
                if os.path.isfile(settingsfile):
                    with codecs.open(settingsfile, encoding=encoding,
                                     mode="r") as f:
                        self.__dict__ = json.load(f, encoding=encoding)
                else:
                    self._set_default()
            except Exception as ex:
                helpers.get_logger().exception(
                    "Failed to load setting: " + str(ex)
                )
                self._set_default()

    def reload(self, jsondata, encoding="utf-8"):
        """
        Reload settings from Chatbot user interface by given json data.
        """
        self.__dict__ = json.loads(jsondata, encoding=encoding)

        ScoreSettings._reload_event.emit(
            config.SettingsReloadEventName, self
        )

    def save(self, settingsfile, encoding="utf-8"):
        """
        Save settings contained within to .json and .js settings files.
        """
        helpers.save_json(self.__dict__, settingsfile)

        with codecs.open(settingsfile.replace("json", "js"),
                         encoding=encoding, mode="w+") as f:
            content = (
                "var settings = {0};".format(
                    json.dumps(self.__dict__, encoding=encoding)
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
        self.CommandGetScore = config.CommandGetScore
        self.CommandGetScoreCooldown = config.CommandGetScoreCooldown
        self.CommandCreateScore = config.CommandCreateScore
        self.CommandCreateScoreCooldown = config.CommandCreateScoreCooldown
        self.CommandUpdateScore = config.CommandUpdateScore
        self.CommandUpdateScoreCooldown = config.CommandUpdateScoreCooldown
        self.CommandResetScore = config.CommandResetScore
        self.CommandResetScoreCooldown = config.CommandResetScoreCooldown
        self.CommandDeleteScore = config.CommandDeleteScore
        self.CommandDeleteScoreCooldown = config.CommandDeleteScoreCooldown

        # Permission group.
        self.PermissionOnGet = config.PermissionOnGet
        self.PermissionInfoOnGet = config.PermissionInfoOnGet
        self.PermissionOnEdit = config.PermissionOnEdit
        self.PermissionInfoOnEdit = config.PermissionInfoOnEdit
        self.PermissionDeniedMessage = config.PermissionDeniedMessage

        # Chat Messages group.
        self.InvalidCommandCallMessage = config.InvalidCommandCallMessage
        self.NoScoreFoundMessage = config.NoScoreFoundMessage
        self.CurrentScoreMessage = config.CurrentScoreMessage
        self.CreatedScoreMessage = config.CreatedScoreMessage
        self.RecreatedScoreMessage = config.RecreatedScoreMessage
        self.NothingToUpdateMessage = config.NothingToUpdateMessage
        self.InvalidScoreValueMessage = config.InvalidScoreValueMessage
        self.UpdatedScoreMessage = config.UpdatedScoreMessage
        self.NothingToResetMessage = config.NothingToResetMessage
        self.ResetScoreMessage = config.ResetScoreMessage
        self.NothingToDeleteMessage = config.NothingToDeleteMessage
        self.DeletedScoreMessage = config.DeletedScoreMessage
        self.TimeRemainingMessage = config.TimeRemainingMessage

        # Debugging group.
        self.LoggingLevel = config.LoggingLevel
        self.AllowLoggingToFile = config.AllowLoggingToFile

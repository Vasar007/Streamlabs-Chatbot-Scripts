# -*- coding: utf-8 -*-

import os
import codecs
import json

import song_request_config as config
import song_request_helpers as helpers
from song_request_event_emitter import SongRequestEventEmitter as EventEmitter 


class SongRequestSettings(object):

    _reload_event = EventEmitter()

    def __init__(self, settingsfile=None, encoding="utf-8"):
        """
        Load in saved settings file if available or else set default values.
        """
        self.encoding = encoding
        if settingsfile is None:
            self._set_default()
        else:
            try:
                if os.path.isfile(settingsfile):
                    with codecs.open(settingsfile, encoding=self.encoding,
                                     mode="r") as f:
                        self.__dict__ = json.load(f, encoding=self.encoding)
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
        self.__dict__ = json.loads(jsondata, encoding=self.encoding)

        SongRequestSettings._reload_event.emit(
            config.SettingsReloadEventName, self
        )

    def save(self, settingsfile):
        """
        Save settings contained within to .json and .js settings files.
        """
        helpers.save_json(self.__dict__, settingsfile)

        with codecs.open(settingsfile.replace("json", "js"),
                         encoding=self.encoding, mode="w+") as f:
            content = (
                "var settings = {0};".format(
                    json.dumps(self.__dict__, encoding=self.encoding)
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
        self.CommandAddSongRequest = config.CommandAddSongRequest
        self.CommandAddSongRequestCooldown = config.CommandAddSongRequestCooldown
        self.CommandCancelSongRequest = config.CommandCancelSongRequest
        self.CommandCancelSongRequestCooldown = config.CommandCancelSongRequestCooldown
        self.CommandApproveSongRequest = config.CommandApproveSongRequest
        self.CommandApproveSongRequestCooldown = config.CommandApproveSongRequestCooldown
        self.CommandRejectSongRequest = config.CommandRejectSongRequest
        self.CommandRejectSongRequestCooldown = config.CommandRejectSongRequestCooldown
        self.CommandGetSongRequest = config.CommandGetSongRequest
        self.CommandGetSongRequestCooldown = config.CommandGetSongRequestCooldown
        self.CommandUseWhisperSongRequest = config.CommandUseWhisperSongRequest
        self.CommandUseWhisperSongRequestCooldown = config.CommandUseWhisperSongRequestCooldown
        self.HttpPageLinkToParse = config.HttpPageLinkToParse
        self.NumberOfSongRequestsToAdd = config.NumberOfSongRequestsToAdd
        self.UseWhisperMessagesToControlSongRequests = config.UseWhisperMessagesToControlSongRequests
        self.BrowserDriverPath = config.BrowserDriverPath
        self.SelectedBrowserDriver = config.SelectedBrowserDriver
        self.ElementIdOfNewSongTextField = config.ElementIdOfNewSongTextField
        self.ElementIdOfAddSongButton = config.ElementIdOfAddSongButton
        self.ClassNameOfNotificationIcon = config.ClassNameOfNotificationIcon
        self.ClassNameOfSuccessNotificationIcon = config.ClassNameOfSuccessNotificationIcon
        self.ClassNameOfErrorNotificationIcon = config.ClassNameOfErrorNotificationIcon
        self.ClassNameOfNotificationDescription = config.ClassNameOfNotificationDescription

        # Permission group.
        self.PermissionOnAddCancelSongRequest = config.PermissionOnAddCancelSongRequest
        self.PermissionInfoOnAddCancelSongRequest = config.PermissionInfoOnAddCancelSongRequest
        self.PermissionOnApproveRejectGetSongRequest = config.PermissionOnApproveRejectGetSongRequest
        self.PermissionInfoOnApproveRejectGetSongRequest = config.PermissionInfoOnApproveRejectGetSongRequest
        self.PermissionDeniedMessage = config.PermissionDeniedMessage

        # Chat Messages group.
        self.InvalidCommandCallMessage = config.InvalidCommandCallMessage
        self.ResponseMessage = config.ResponseMessage
        self.TimeRemainingMessage = config.TimeRemainingMessage

        # Debugging group.
        self.LoggingLevel = config.LoggingLevel
        self.AllowLoggingToFile = config.AllowLoggingToFile

# -*- coding: utf-8 -*-

import os
import codecs
import json

import song_request_config as config
import song_request_helpers as helpers
from song_request_event_emitter import SongRequestEventEmitter as EventEmitter 

from Scripts.SongRequest.CSharp.Models.Settings import ISongRequestScriptSettings
from Scripts.SongRequest.CSharp.Models.Settings import WebDriverType


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
        self.MaxNumberOfSongRequestsToAdd = config.MaxNumberOfSongRequestsToAdd
        self.UseWhisperMessagesToControlSongRequests = config.UseWhisperMessagesToControlSongRequests
        self.DispatchTimeoutInSeconds = config.DispatchTimeoutInSeconds
        self.TimeoutToWaitInMilliseconds = config.TimeoutToWaitInMilliseconds
        self.BrowserDriverPath = config.BrowserDriverPath
        self.BrowserDriverExecutableName = config.BrowserDriverExecutableName
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
        self.TimeRemainingMessage = config.TimeRemainingMessage
        self.MaxLimitOfSongRequestsIsExceededMessage = config.MaxLimitOfSongRequestsIsExceededMessage
        self.InvalidTargetMessage = config.InvalidTargetMessage
        self.NoSongRequestsMessage = config.NoSongRequestsMessage
        self.NonExistentSongRequestNumberMessage = config.NonExistentSongRequestNumberMessage
        self.SongRequestAddedMessage = config.SongRequestAddedMessage
        self.SongRequestToApproveMessage = config.SongRequestToApproveMessage
        self.SongRequestApprovedMessage = config.SongRequestApprovedMessage
        self.OnSuccessSongRequestMessage = config.OnSuccessSongRequestMessage
        self.OnFailureSongRequestDefaultErrorMessage = config.OnFailureSongRequestDefaultErrorMessage
        self.OnFailureSongRequestMessage = config.OnFailureSongRequestMessage
        self.SongRequestRejectedMessage = config.SongRequestRejectedMessage
        self.SongRequestDefaultRejectReason = config.SongRequestDefaultRejectReason
        self.SongRequestCancelMessage = config.SongRequestCancelMessage

        # Debugging group.
        self.LoggingLevel = config.LoggingLevel
        self.AllowLoggingToFile = config.AllowLoggingToFile
        self.EnableWebDriverDebug = config.EnableWebDriverDebug


class SongRequestCSharpSettings(ISongRequestScriptSettings):

    def __init__(self, settings):
        self.settings = settings

    # Implementation of ISongRequestScriptSettings

    # Setup group.
    @property
    def CommandAddSongRequest(self):
        return self.settings.CommandAddSongRequest

    @property
    def CommandAddSongRequestCooldown(self):
        return self.settings.CommandAddSongRequestCooldown

    @property
    def CommandCancelSongRequest(self):
        return self.settings.CommandCancelSongRequest

    @property
    def CommandCancelSongRequestCooldown(self):
        return self.settings.CommandCancelSongRequestCooldown

    @property
    def CommandApproveSongRequest(self):
        return self.settings.CommandApproveSongRequest

    @property
    def CommandApproveSongRequestCooldown(self):
        return self.settings.CommandApproveSongRequestCooldown

    @property
    def CommandRejectSongRequest(self):
        return self.settings.CommandRejectSongRequest

    @property
    def CommandRejectSongRequestCooldown(self):
        return self.settings.CommandRejectSongRequestCooldown

    @property
    def CommandGetSongRequest(self):
        return self.settings.CommandGetSongRequest

    @property
    def CommandGetSongRequestCooldown(self):
        return self.settings.CommandGetSongRequestCooldown

    @property
    def CommandUseWhisperSongRequest(self):
        return self.settings.CommandUseWhisperSongRequest

    @property
    def CommandUseWhisperSongRequestCooldown(self):
        return self.settings.CommandUseWhisperSongRequestCooldown

    @property
    def HttpPageLinkToParse(self):
        return helpers.wrap_http_link(self.settings.HttpPageLinkToParse)

    @property
    def NumberOfSongRequestsToAdd(self):
        return self.settings.NumberOfSongRequestsToAdd

    @property
    def UseWhisperMessagesToControlSongRequests(self):
        return self.settings.UseWhisperMessagesToControlSongRequests

    @property
    def DispatchTimeoutInSeconds(self):
        return self.settings.DispatchTimeoutInSeconds

    @property
    def TimeoutToWaitInMilliseconds(self):
        return self.settings.TimeoutToWaitInMilliseconds

    @property
    def BrowserDriverPath(self):
        return helpers.wrap_file_path(self.settings.BrowserDriverPath)

    @property
    def BrowserDriverExecutableName(self):
        return helpers.wrap_file_name(self.settings.BrowserDriverExecutableName)

    @property
    def SelectedBrowserDriver(self):
        return WebDriverType.Wrap(self.settings.SelectedBrowserDriver)

    @property
    def ElementIdOfNewSongTextField(self):
        return self.settings.ElementIdOfNewSongTextField

    @property
    def ElementIdOfAddSongButton(self):
        return self.settings.ElementIdOfAddSongButton

    @property
    def ClassNameOfNotificationIcon(self):
        return self.settings.ClassNameOfNotificationIcon

    @property
    def ClassNameOfSuccessNotificationIcon(self):
        return self.settings.ClassNameOfSuccessNotificationIcon

    @property
    def ClassNameOfErrorNotificationIcon(self):
        return self.settings.ClassNameOfErrorNotificationIcon

    @property
    def ClassNameOfNotificationDescription(self):
        return self.settings.ClassNameOfNotificationDescription

    # Permission group.
    @property
    def PermissionOnAddCancelSongRequest(self):
        return self.settings.PermissionOnAddCancelSongRequest

    @property
    def PermissionInfoOnAddCancelSongRequest(self):
        return self.settings.PermissionInfoOnAddCancelSongRequest

    @property
    def PermissionOnApproveRejectGetSongRequest(self):
        return self.settings.PermissionOnApproveRejectGetSongRequest

    @property
    def PermissionInfoOnApproveRejectGetSongRequest(self):
        return self.settings.PermissionInfoOnApproveRejectGetSongRequest

    @property
    def PermissionDeniedMessage(self):
        return self.settings.PermissionDeniedMessage
    
    # Chat Messages group.
    @property
    def InvalidCommandCallMessage(self):
        return self.settings.InvalidCommandCallMessage

    @property
    def TimeRemainingMessage(self):
        return self.settings.TimeRemainingMessage

    @property
    def MaxLimitOfSongRequestsIsExceededMessage(self):
        return self.settings.MaxLimitOfSongRequestsIsExceededMessage

    @property
    def InvalidTargetMessage(self):
        return self.settings.InvalidTargetMessage

    @property
    def NoSongRequestsMessage(self):
        return self.settings.NoSongRequestsMessage

    @property
    def NonExistentSongRequestNumberMessage(self):
        return self.settings.NonExistentSongRequestNumberMessage

    @property
    def SongRequestAddedMessage(self):
        return self.settings.SongRequestAddedMessage

    @property
    def SongRequestToApproveMessage(self):
        return self.settings.SongRequestToApproveMessage

    @property
    def SongRequestApprovedMessage(self):
        return self.settings.SongRequestApprovedMessage

    @property
    def OnSuccessSongRequestMessage(self):
        return self.settings.OnSuccessSongRequestMessage

    @property
    def OnFailureSongRequestMessage(self):
        return self.settings.OnFailureSongRequestMessage

    @property
    def OnFailureSongRequestDefaultErrorMessage(self):
        return self.settings.OnFailureSongRequestDefaultErrorMessage

    @property
    def SongRequestRejectedMessage(self):
        return self.settings.SongRequestRejectedMessage

    @property
    def SongRequestDefaultRejectReason(self):
        return self.settings.SongRequestDefaultRejectReason

    @property
    def SongRequestCancelMessage(self):
        return self.settings.SongRequestCancelMessage

    # Debugging group.
    @property
    def LoggingLevel(self):
        return self.settings.LoggingLevel

    @property
    def AllowLoggingToFile(self):
        return self.settings.AllowLoggingToFile

    @property
    def EnableWebDriverDebug(self):
        return self.settings.EnableWebDriverDebug

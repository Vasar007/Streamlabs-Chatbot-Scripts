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

        SongRequestSettings._reload_event.emit(
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

    def parse_mod_ids(self, logger):
        if not self.UseWhisperMessagesToControlSongRequests:
            logger.info("Whisper option is turn off.")
            return [""]

        raw_mod_ids = self.ModIdsToWhisper
        mod_ids = raw_mod_ids.split(config.DefaultDelimeter)
        for i in range(len(mod_ids)):
            temp_mod_id = mod_ids[i]
            mod_ids[i] = temp_mod_id.strip()

        logger.info("Using mod IDs to whisper: {0}".format(mod_ids))
        return mod_ids

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
        self.CommandSkipSongRequest = config.CommandSkipSongRequest
        self.CommandSkipSongRequestCooldown = config.CommandSkipSongRequestCooldown
        self.CommandOptionSongRequest = config.CommandOptionSongRequest
        self.CommandOptionSongRequestCooldown = config.CommandOptionSongRequestCooldown
        self.HttpPageLinkToParse = config.HttpPageLinkToParse
        self.MaxNumberOfSongRequestsToAdd = config.MaxNumberOfSongRequestsToAdd
        self.WaitingTimeoutForSongRequestsInSeconds = config.WaitingTimeoutForSongRequestsInSeconds
        self.DispatchTimeoutInSeconds = config.DispatchTimeoutInSeconds
        self.TimeoutToWaitInMilliseconds = config.TimeoutToWaitInMilliseconds
        self.UseWhisperMessagesToControlSongRequests = config.UseWhisperMessagesToControlSongRequests
        self.ModIdsToWhisper = config.ModIdsToWhisper
        self.LowMessageMode = config.LowMessageMode
        self.EnableCommandProcessing = config.EnableCommandProcessing
        self.EnableLinkValidation = config.EnableLinkValidation

        # Parsing group.
        self.SelectedBrowserDriver = config.SelectedBrowserDriver
        self.BrowserDriverPath = config.BrowserDriverPath
        self.BrowserDriverExecutableName = config.BrowserDriverExecutableName
        self.ElementIdOfNewSongTextField = config.ElementIdOfNewSongTextField
        self.ElementIdOfAddSongButton = config.ElementIdOfAddSongButton
        self.ClassNameOfNotificationIcon = config.ClassNameOfNotificationIcon
        self.ClassNameOfSuccessNotificationIcon = config.ClassNameOfSuccessNotificationIcon
        self.ClassNameOfErrorNotificationIcon = config.ClassNameOfErrorNotificationIcon
        self.ClassNameOfNotificationDescription = config.ClassNameOfNotificationDescription
        self.ElementIdOfSkipSongButton = config.ElementIdOfSkipSongButton
        self.ElementIdOfRemoveQueueSongButton = config.ElementIdOfRemoveQueueSongButton

        # Permission group.
        self.PermissionOnAddCancelSongRequest = config.PermissionOnAddCancelSongRequest
        self.PermissionInfoOnAddCancelSongRequest = config.PermissionInfoOnAddCancelSongRequest
        self.PermissionOnManageSongRequest = config.PermissionOnManageSongRequest
        self.PermissionInfoOnManageSongRequest = config.PermissionInfoOnManageSongRequest
        self.PermissionDeniedMessage = config.PermissionDeniedMessage

        # Chat Messages group.
        self.InvalidCommandCallMessage = config.InvalidCommandCallMessage
        self.TimeRemainingMessage = config.TimeRemainingMessage
        self.MaxLimitOfSongRequestsIsExceededMessage = config.MaxLimitOfSongRequestsIsExceededMessage
        self.InvalidTargetMessage = config.InvalidTargetMessage
        self.NoSongRequestsMessage = config.NoSongRequestsMessage
        self.NonExistentSongRequestNumberMessage = config.NonExistentSongRequestNumberMessage
        self.SongRequestDecisionReasonMessage = config.SongRequestDecisionReasonMessage
        self.SongRequestAddedMessage = config.SongRequestAddedMessage
        self.SongRequestToApproveMessage = config.SongRequestToApproveMessage
        self.SongRequestApprovedMessage = config.SongRequestApprovedMessage
        self.OnSuccessSongRequestMessage = config.OnSuccessSongRequestMessage
        self.OnSuccessSongRequestDefaultResultMessage = config.OnSuccessSongRequestDefaultResultMessage
        self.OnFailureSongRequestDefaultErrorMessage = config.OnFailureSongRequestDefaultErrorMessage
        self.OnFailureSongRequestMessage = config.OnFailureSongRequestMessage
        self.SongRequestRejectedMessage = config.SongRequestRejectedMessage
        self.SongRequestDefaultRejectReason = config.SongRequestDefaultRejectReason
        self.SongRequestCancelMessage = config.SongRequestCancelMessage
        self.GotUserSongRequestsMessage = config.GotUserSongRequestsMessage
        self.NoUserSongRequestsMessage = config.NoUserSongRequestsMessage
        self.OptionValueTheSameMessage = config.OptionValueTheSameMessage
        self.OptionValueChangedMessage = config.OptionValueChangedMessage
        self.FailedToSetOptionMessage = config.FailedToSetOptionMessage
        self.FailedToSetOptionInvalidTypeMessage = config.FailedToSetOptionInvalidTypeMessage
        self.FailedToSetOptionInvalidNameMessage = config.FailedToSetOptionInvalidNameMessage
        self.FailedToValidateLinkMessage = config.FailedToValidateLinkMessage
        self.CommandProcessingDisabledMessage = config.CommandProcessingDisabledMessage
        self.SkipAllSongRequestsMessage = config.SkipAllSongRequestsMessage
        self.SkipCurrentSongRequestMessage = config.SkipCurrentSongRequestMessage
        self.NoSongRequestsToSkipMessage = config.NoSongRequestsToSkipMessage
        self.FailedToSkipSongRequestsMessage = config.FailedToSkipSongRequestsMessage

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
    def CommandSkipSongRequest(self):
        return self.settings.CommandSkipSongRequest

    @property
    def CommandSkipSongRequestCooldown(self):
        return self.settings.CommandSkipSongRequestCooldown

    @property
    def CommandOptionSongRequest(self):
        return self.settings.CommandOptionSongRequest

    @property
    def CommandOptionSongRequestCooldown(self):
        return self.settings.CommandOptionSongRequestCooldown

    @property
    def HttpPageLinkToParse(self):
        return helpers.wrap_http_link(self.settings.HttpPageLinkToParse)

    @property
    def NumberOfSongRequestsToAdd(self):
        return self.settings.NumberOfSongRequestsToAdd

    @property
    def WaitingTimeoutForSongRequestsInSeconds(self):
        return self.settings.WaitingTimeoutForSongRequestsInSeconds

    @property
    def DispatchTimeoutInSeconds(self):
        return self.settings.DispatchTimeoutInSeconds

    @property
    def TimeoutToWaitInMilliseconds(self):
        return self.settings.TimeoutToWaitInMilliseconds

    @property
    def UseWhisperMessagesToControlSongRequests(self):
        return self.settings.UseWhisperMessagesToControlSongRequests

    @property
    def ModIdsToWhisper(self):
        return self.settings.ModIdsToWhisper

    @property
    def LowMessageMode(self):
        return self.settings.LowMessageMode

    @property
    def EnableCommandProcessing(self):
        return self.settings.EnableCommandProcessing

    @property
    def EnableLinkValidation(self):
        return self.settings.EnableLinkValidation

    # Parsing group.
    @property
    def SelectedBrowserDriver(self):
        return WebDriverType.Wrap(self.settings.SelectedBrowserDriver)

    @property
    def BrowserDriverPath(self):
        return helpers.wrap_file_path(self.settings.BrowserDriverPath)

    @property
    def BrowserDriverExecutableName(self):
        return helpers.wrap_file_name(self.settings.BrowserDriverExecutableName)

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

    @property
    def ElementIdOfSkipSongButton(self):
        return self.settings.ElementIdOfSkipSongButton

    @property
    def ElementIdOfRemoveQueueSongButton(self):
        return self.settings.ElementIdOfRemoveQueueSongButton

    # Permission group.
    @property
    def PermissionOnAddCancelSongRequest(self):
        return self.settings.PermissionOnAddCancelSongRequest

    @property
    def PermissionInfoOnAddCancelSongRequest(self):
        return self.settings.PermissionInfoOnAddCancelSongRequest

    @property
    def PermissionOnManageSongRequest(self):
        return self.settings.PermissionOnManageSongRequest

    @property
    def PermissionInfoOnManageSongRequest(self):
        return self.settings.PermissionInfoOnManageSongRequest

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
    def SongRequestDecisionReasonMessage(self):
        return self.settings.SongRequestDecisionReasonMessage

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
    def OnSuccessSongRequestDefaultResultMessage(self):
        return self.settings.OnSuccessSongRequestDefaultResultMessage

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

    @property
    def GotUserSongRequestsMessage(self):
        return self.settings.GotUserSongRequestsMessage

    @property
    def NoUserSongRequestsMessage(self):
        return self.settings.NoUserSongRequestsMessage

    @property
    def OptionValueTheSameMessage(self):
        return self.settings.OptionValueTheSameMessage

    @property
    def OptionValueChangedMessage(self):
        return self.settings.OptionValueChangedMessage

    @property
    def FailedToSetOptionMessage(self):
        return self.settings.FailedToSetOptionMessage

    @property
    def FailedToSetOptionInvalidTypeMessage(self):
        return self.settings.FailedToSetOptionInvalidTypeMessage

    @property
    def FailedToSetOptionInvalidNameMessage(self):
        return self.settings.FailedToSetOptionInvalidNameMessage

    @property
    def FailedToValidateLinkMessage(self):
        return self.settings.FailedToValidateLinkMessage

    @property
    def CommandProcessingDisabledMessage(self):
        return self.settings.CommandProcessingDisabledMessage

    @property
    def SkipAllSongRequestsMessage(self):
        return self.settings.SkipAllSongRequestsMessage

    @property
    def SkipCurrentSongRequestMessage(self):
        return self.settings.SkipCurrentSongRequestMessage

    @property
    def NoSongRequestsToSkipMessage(self):
        return self.settings.NoSongRequestsToSkipMessage

    @property
    def FailedToSkipSongRequestsMessage(self):
        return self.settings.FailedToSkipSongRequestsMessage

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

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

    def update_settings_on_the_fly(self, logger, messenger, settingsfile,
                                   data_wrapper):
        raw_user_id = data_wrapper.user_id
        raw_user_name = data_wrapper.user_name

        option_name = data_wrapper.get_param(1)
        param_count = data_wrapper.get_param_count()

        raw_new_value = ""
        for i in range(2, param_count):
            raw_new_value += " " + data_wrapper.get_param(i)
        raw_new_value = raw_new_value.strip()

        logger.info(
            "User {0} wants to change option {1} to {2}"
            .format(raw_user_id, option_name, raw_new_value)
        )

        message = None
        try:
            previous_value = self.__dict__[option_name]
            previous_value_type = type(previous_value)
            new_value = helpers.safe_cast_with_guess(
                raw_new_value, previous_value_type
            )

            if new_value is None:
                submessage = (
                    self.FailedToSetOptionInvalidTypeMessage
                    .format(previous_value_type)
                )
                message = (
                    self.FailedToSetOptionMessage
                    .format(raw_user_name, option_name, submessage)
                )
            elif previous_value == new_value:
                message = (
                    self.OptionValueTheSameMessage
                    .format(raw_user_name, option_name, previous_value, new_value)
                )
            else:
                self.__dict__[option_name] = new_value
                message = (
                    self.OptionValueChangedMessage
                    .format(raw_user_name, option_name, previous_value, new_value)
                )

            self.save(settingsfile)
            logger.info(message)
        except KeyError as key_error:
            submessage = self.FailedToSetOptionInvalidNameMessage
            message = (
                self.FailedToSetOptionMessage
                .format(raw_user_name, option_name, submessage)
            )
            logger.exception(message)
        except Exception as ex:
            message = (
                self.FailedToSetOptionMessage
                .format(raw_user_name, option_name, str(ex))
            )
            logger.exception(message)

        messenger.send_message(raw_user_id, message)

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

    def _are_strings_equal(self, value1, value2):
        return value1.lower() == value2.lower()

    def is_all_parameter(self, value):
        return self._are_strings_equal(value, self.ParameterAll)

    def is_user_subcommand(self, value):
        return self._are_strings_equal(value, config.SubcommandChangeUserOption)

    def is_reset_subcommand(self, value):
        return self._are_strings_equal(value, config.SubcommandResetNumberOfOrderedSongRequests)

    def _set_default(self):
        # Commands group.
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
        self.ParameterAll = config.ParameterAll

        # Setup group.
        self.HttpPageLinkToParse = config.HttpPageLinkToParse
        self.MaxNumberOfSongRequestsToAdd = config.MaxNumberOfSongRequestsToAdd
        self.WaitingTimeoutForSongRequestsInSeconds = config.WaitingTimeoutForSongRequestsInSeconds
        self.DispatchTimeoutInSeconds = config.DispatchTimeoutInSeconds
        self.TimeoutToWaitBetweenSongRequestsInSeconds = config.TimeoutToWaitBetweenSongRequestsInSeconds
        self.TimeoutToWaitInMilliseconds = config.TimeoutToWaitInMilliseconds
        self.UseWhisperMessagesToControlSongRequests = config.UseWhisperMessagesToControlSongRequests
        self.ModIdsToWhisper = config.ModIdsToWhisper
        self.LowMessageMode = config.LowMessageMode
        self.EnableCommandProcessing = config.EnableCommandProcessing
        self.EnableLinkValidation = config.EnableLinkValidation
        self.FilterNonChatMessages = config.FilterNonChatMessages

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
        self.OptionValueTheSameMessage = config.OptionValueTheSameMessage
        self.OptionValueChangedMessage = config.OptionValueChangedMessage
        self.FailedToSetOptionMessage = config.FailedToSetOptionMessage
        self.FailedToSetOptionInvalidTypeMessage = config.FailedToSetOptionInvalidTypeMessage
        self.FailedToSetOptionInvalidNameMessage = config.FailedToSetOptionInvalidNameMessage
        self.ResetUserSongRequestOptionsMessage = config.ResetUserSongRequestOptionsMessage
        self.InvalidOptionsSubcommandMessage = config.InvalidOptionsSubcommandMessage
        self.MaxLimitOfSongRequestsIsExceededMessage = config.MaxLimitOfSongRequestsIsExceededMessage
        self.InvalidTargetMessage = config.InvalidTargetMessage
        self.SongRequestNumberAndLinkFormat = config.SongRequestNumberAndLinkFormat
        self.ProcessedSongRequestNumberAndLinkFormat = config.ProcessedSongRequestNumberAndLinkFormat
        self.AutoApproveReason = config.AutoApproveReason
        self.NoSongRequestsMessage = config.NoSongRequestsMessage
        self.NonExistentSongRequestNumberMessage = config.NonExistentSongRequestNumberMessage
        self.AlreadyProcessedSongRequestMessage = config.AlreadyProcessedSongRequestMessage
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
        self._settings = settings

    # Implementation of ISongRequestScriptSettings

    # Commands group.
    @property
    def CommandAddSongRequest(self):
        return self._settings.CommandAddSongRequest

    @property
    def CommandAddSongRequestCooldown(self):
        return self._settings.CommandAddSongRequestCooldown

    @property
    def CommandCancelSongRequest(self):
        return self._settings.CommandCancelSongRequest

    @property
    def CommandCancelSongRequestCooldown(self):
        return self._settings.CommandCancelSongRequestCooldown

    @property
    def CommandApproveSongRequest(self):
        return self._settings.CommandApproveSongRequest

    @property
    def CommandApproveSongRequestCooldown(self):
        return self._settings.CommandApproveSongRequestCooldown

    @property
    def CommandRejectSongRequest(self):
        return self._settings.CommandRejectSongRequest

    @property
    def CommandRejectSongRequestCooldown(self):
        return self._settings.CommandRejectSongRequestCooldown

    @property
    def CommandGetSongRequest(self):
        return self._settings.CommandGetSongRequest

    @property
    def CommandGetSongRequestCooldown(self):
        return self._settings.CommandGetSongRequestCooldown

    @property
    def CommandSkipSongRequest(self):
        return self._settings.CommandSkipSongRequest

    @property
    def CommandSkipSongRequestCooldown(self):
        return self._settings.CommandSkipSongRequestCooldown

    @property
    def ParameterAll(self):
        return self._settings.ParameterAll

    # Setup group.
    @property
    def HttpPageLinkToParse(self):
        return helpers.wrap_http_link(self._settings.HttpPageLinkToParse)

    @property
    def NumberOfSongRequestsToAdd(self):
        return self._settings.NumberOfSongRequestsToAdd

    @property
    def WaitingTimeoutForSongRequestsInSeconds(self):
        return self._settings.WaitingTimeoutForSongRequestsInSeconds

    @property
    def DispatchTimeoutInSeconds(self):
        return self._settings.DispatchTimeoutInSeconds

    @property
    def TimeoutToWaitBetweenSongRequestsInSeconds(self):
        return self._settings.TimeoutToWaitBetweenSongRequestsInSeconds

    @property
    def TimeoutToWaitInMilliseconds(self):
        return self._settings.TimeoutToWaitInMilliseconds

    @property
    def UseWhisperMessagesToControlSongRequests(self):
        return self._settings.UseWhisperMessagesToControlSongRequests

    @property
    def ModIdsToWhisper(self):
        return self._settings.ModIdsToWhisper

    @property
    def LowMessageMode(self):
        return self._settings.LowMessageMode

    @property
    def EnableCommandProcessing(self):
        return self._settings.EnableCommandProcessing

    @property
    def EnableLinkValidation(self):
        return self._settings.EnableLinkValidation

    @property
    def FilterNonChatMessages(self):
        return self._settings.FilterNonChatMessages

    # Parsing group.
    @property
    def SelectedBrowserDriver(self):
        return WebDriverType.Wrap(self._settings.SelectedBrowserDriver)

    @property
    def BrowserDriverPath(self):
        return helpers.wrap_file_path(self._settings.BrowserDriverPath)

    @property
    def BrowserDriverExecutableName(self):
        return helpers.wrap_file_name(self._settings.BrowserDriverExecutableName)

    @property
    def ElementIdOfNewSongTextField(self):
        return self._settings.ElementIdOfNewSongTextField

    @property
    def ElementIdOfAddSongButton(self):
        return self._settings.ElementIdOfAddSongButton

    @property
    def ClassNameOfNotificationIcon(self):
        return self._settings.ClassNameOfNotificationIcon

    @property
    def ClassNameOfSuccessNotificationIcon(self):
        return self._settings.ClassNameOfSuccessNotificationIcon

    @property
    def ClassNameOfErrorNotificationIcon(self):
        return self._settings.ClassNameOfErrorNotificationIcon

    @property
    def ClassNameOfNotificationDescription(self):
        return self._settings.ClassNameOfNotificationDescription

    @property
    def ElementIdOfSkipSongButton(self):
        return self._settings.ElementIdOfSkipSongButton

    @property
    def ElementIdOfRemoveQueueSongButton(self):
        return self._settings.ElementIdOfRemoveQueueSongButton

    # Permission group.
    @property
    def PermissionOnAddCancelSongRequest(self):
        return self._settings.PermissionOnAddCancelSongRequest

    @property
    def PermissionInfoOnAddCancelSongRequest(self):
        return self._settings.PermissionInfoOnAddCancelSongRequest

    @property
    def PermissionOnManageSongRequest(self):
        return self._settings.PermissionOnManageSongRequest

    @property
    def PermissionInfoOnManageSongRequest(self):
        return self._settings.PermissionInfoOnManageSongRequest

    @property
    def PermissionDeniedMessage(self):
        return self._settings.PermissionDeniedMessage
    
    # Chat Messages group.
    @property
    def InvalidCommandCallMessage(self):
        return self._settings.InvalidCommandCallMessage

    @property
    def TimeRemainingMessage(self):
        return self._settings.TimeRemainingMessage

    @property
    def OptionValueTheSameMessage(self):
        return self._settings.OptionValueTheSameMessage

    @property
    def OptionValueChangedMessage(self):
        return self._settings.OptionValueChangedMessage

    @property
    def FailedToSetOptionMessage(self):
        return self._settings.FailedToSetOptionMessage

    @property
    def FailedToSetOptionInvalidTypeMessage(self):
        return self._settings.FailedToSetOptionInvalidTypeMessage

    @property
    def FailedToSetOptionInvalidNameMessage(self):
        return self._settings.FailedToSetOptionInvalidNameMessage

    @property
    def ResetUserSongRequestOptionsMessage(self):
        return self._settings.ResetUserSongRequestOptionsMessage

    @property
    def InvalidOptionsSubcommandMessage(self):
        return self._settings.InvalidOptionsSubcommandMessage

    @property
    def MaxLimitOfSongRequestsIsExceededMessage(self):
        return self._settings.MaxLimitOfSongRequestsIsExceededMessage

    @property
    def InvalidTargetMessage(self):
        return self._settings.InvalidTargetMessage

    @property
    def SongRequestNumberAndLinkFormat(self):
        return self._settings.SongRequestNumberAndLinkFormat

    @property
    def ProcessedSongRequestNumberAndLinkFormat(self):
        return self._settings.ProcessedSongRequestNumberAndLinkFormat

    @property
    def AutoApproveReason(self):
        return self._settings.AutoApproveReason

    @property
    def NoSongRequestsMessage(self):
        return self._settings.NoSongRequestsMessage

    @property
    def NonExistentSongRequestNumberMessage(self):
        return self._settings.NonExistentSongRequestNumberMessage

    @property
    def AlreadyProcessedSongRequestMessage(self):
        return self._settings.AlreadyProcessedSongRequestMessage

    @property
    def SongRequestDecisionReasonMessage(self):
        return self._settings.SongRequestDecisionReasonMessage

    @property
    def SongRequestAddedMessage(self):
        return self._settings.SongRequestAddedMessage

    @property
    def SongRequestToApproveMessage(self):
        return self._settings.SongRequestToApproveMessage

    @property
    def SongRequestApprovedMessage(self):
        return self._settings.SongRequestApprovedMessage

    @property
    def OnSuccessSongRequestMessage(self):
        return self._settings.OnSuccessSongRequestMessage

    @property
    def OnSuccessSongRequestDefaultResultMessage(self):
        return self._settings.OnSuccessSongRequestDefaultResultMessage

    @property
    def OnFailureSongRequestMessage(self):
        return self._settings.OnFailureSongRequestMessage

    @property
    def OnFailureSongRequestDefaultErrorMessage(self):
        return self._settings.OnFailureSongRequestDefaultErrorMessage

    @property
    def SongRequestRejectedMessage(self):
        return self._settings.SongRequestRejectedMessage

    @property
    def SongRequestDefaultRejectReason(self):
        return self._settings.SongRequestDefaultRejectReason

    @property
    def SongRequestCancelMessage(self):
        return self._settings.SongRequestCancelMessage

    @property
    def GotUserSongRequestsMessage(self):
        return self._settings.GotUserSongRequestsMessage

    @property
    def NoUserSongRequestsMessage(self):
        return self._settings.NoUserSongRequestsMessage

    @property
    def FailedToValidateLinkMessage(self):
        return self._settings.FailedToValidateLinkMessage

    @property
    def CommandProcessingDisabledMessage(self):
        return self._settings.CommandProcessingDisabledMessage

    @property
    def SkipAllSongRequestsMessage(self):
        return self._settings.SkipAllSongRequestsMessage

    @property
    def SkipCurrentSongRequestMessage(self):
        return self._settings.SkipCurrentSongRequestMessage

    @property
    def NoSongRequestsToSkipMessage(self):
        return self._settings.NoSongRequestsToSkipMessage

    @property
    def FailedToSkipSongRequestsMessage(self):
        return self._settings.FailedToSkipSongRequestsMessage

    # Debugging group.
    @property
    def LoggingLevel(self):
        return self._settings.LoggingLevel

    @property
    def AllowLoggingToFile(self):
        return self._settings.AllowLoggingToFile

    @property
    def EnableWebDriverDebug(self):
        return self._settings.EnableWebDriverDebug

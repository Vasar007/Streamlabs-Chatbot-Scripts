# -*- coding: utf-8 -*-

import os
import logging


# Logging.
LogLevels = {
    "Debug": logging.DEBUG,
    "Info": logging.INFO,
    "Warning": logging.WARNING,
    "Error": logging.ERROR,
    "Off": logging.CRITICAL  # Allow to print only fatal messages.
}

LogFormat = "[%(asctime)s] %(levelname)s    %(message)s"
LogDateFormat = "%d/%m/%Y %H:%M:%S"
LogFileRelativePath = os.path.join("Services", "Scripts", "SongRequest")
LogFileNameFormat = "{0}.log"
LogFileMaxBytes = 10 * 1024 * 1024  # 10 MB
LogFileBackupCount = 10  # Keep last 10 files alive.

LoggingLevel = "Info"
AllowLoggingToFile = False

SettingsReloadEventName = "settings_reload"

# All possible options for permission:
# - Everyone
# - Regular
# - Subscriber
# - GameWisp Subscriber
# - Moderator
# - Editor
# - Invisible
# - User_Specific (info:username)
# - Min_Rank (info:rank)
# - Min_Points (info:points)
# - Min_Hours (info:hours)

Everyone = "everyone"
UserSpecific = "user_specific"
Subscriber = "subscriber"
Moderator = "moderator"
Editor = "editor"

PermissionHierarchy = (Everyone, Subscriber, UserSpecific, Moderator, Editor)

DefaultVersionCommand = "!scripts_info"
DefaultVersionCommandCooldown = 1

CommandOption = "!sr_option"
CommandOptionCooldown = 1
SubcommandChangeUserOption = "user"
SubcommandResetNumberOfOrderedSongRequests = "reset"

CommandAllOptionsUsage = "{0} | {1}"
CommandOptionUsage = "{0} {1} {2}"
CommandManageUserOptionsUsage = "{0} {1} {2} {3}"
ExampleOptionName = "[Option name]"
ExampleOptionValue = "[Option value]"
ExampleSubcommand = "[Subcommand]"

# Values: everyone, moderator, subscriber, user_specific, editor.
PermissionOnDefaultScriptCommands = Moderator
# This field should only be filled when using the user_specific permission.
PermissionInfoOnDefaultScriptCommands = ""

CommandAddCancelGetSkipSongRequestUsage = "{0} {1}"
CommandManageSongRequestUsage = "{0} {1} {2}"
ExampleUserIdOrName = "[UserIdOrName]"
ExampleRequestNumberValidRange = "[1–{0}]"
ExampleYouTubeLinkToSong = "[YouTube link]"
ExampleAllValue = "[{0}]"

DefaultDelimeter = ","

# [Required] Script Information.
ScriptName = "Song Request Script"
Website = "https://github.com/Vasar007/Streamlabs-Chatbot-Scripts"
Description = "Extended song request script."
Creator = "Vasar007"
Version = "1.2.0"

# Command settings and responses (caution: some of the response texts are
# overwritten later/not refactored yet).
CommandAddSongRequest = "!sr"
CommandAddSongRequestCooldown = 1
CommandCancelSongRequest = "!sr_cancel"
CommandCancelSongRequestCooldown = 1
CommandApproveSongRequest = "!sr_approve"
CommandApproveSongRequestCooldown = 1
CommandRejectSongRequest = "!sr_reject"
CommandRejectSongRequestCooldown = 1
CommandGetSongRequest = "!sr_get"
CommandGetSongRequestCooldown = 1
CommandSkipSongRequest = "!sr_skip"
CommandSkipSongRequestCooldown = 1

ParameterAll = "all"

HttpPageLinkToParse = ""
MaxNumberOfSongRequestsToAdd = 1
WaitingTimeoutForSongRequestsInSeconds = 60
DispatchTimeoutInSeconds = 30
TimeoutToWaitBetweenSongRequestsInSeconds = 5
TimeoutToWaitInMilliseconds = 3000
UseWhisperMessagesToControlSongRequests = False
ModIdsToWhisper = ""
LowMessageMode = True
EnableCommandProcessing = True
EnableLinkValidation = True
FilterNonChatMessages = False

EnableWebDriverDebug = False

BrowserDriverPath = "C:\\Program Files\\Common Files\\Webdrivers"
BrowserDriverExecutableName = "chromedriver.exe"
BrowserDriverVersion = "Auto"

EdgeDriver = "Edge"
ChromeDriver = "Chromium/Chrome"
FirefoxDriver = "Firefox"
OperaDriver = "Opera"
SelectedBrowserDriver = ChromeDriver
ElementIdOfNewSongTextField = "newSong"
ElementIdOfAddSongButton = "playerAddSong"
ClassNameOfNotificationIcon = "ui-pnotify-icon"
ClassNameOfSuccessNotificationIcon = "brighttheme-icon-success"
ClassNameOfErrorNotificationIcon = "brighttheme-icon-error"
ClassNameOfNotificationDescription = "ui-pnotify-text"
ElementIdOfSkipSongButton = "playerSkip"
ElementIdOfRemoveQueueSongButton = "queueRemove"

# Values: everyone, moderator, subscriber, user_specific, editor.
PermissionOnAddCancelSongRequest = Subscriber
# This field should only be filled when using the user_specific permission.
PermissionInfoOnAddCancelSongRequest = ""

# Values: everyone, moderator, subscriber, user_specific, editor.
PermissionOnManageSongRequest = Moderator
# This field should only be filled when using the user_specific permission.
PermissionInfoOnManageSongRequest = ""

PermissionDeniedMessage = "Permission denied: You have to be a {0} to use {1} command!"

InvalidCommandCallMessage = "Invalid {0} command call. Usage: {1}"
TimeRemainingMessage = "Command {0} is on cooldown. Time remaining: {1} (seconds)."
OptionValueTheSameMessage = "{0}, option {1} value cannot be changed to the same value [{2}]"
OptionValueChangedMessage = "{0}, option {1} value has been changed from [{2}] to [{3}]"
FailedToSetOptionMessage = "{0}, failed to change option {1}: {2}"
FailedToSetOptionInvalidTypeMessage = "Invalid type (expected: {0})"
FailedToSetOptionInvalidNameMessage = "Invalid option name"
MaxLimitOfSongRequestsIsExceededMessage = "Sorry {0}, you have exceeded max allowed limit of song requests for you per stream ({1})."
InvalidTargetMessage = "Sorry {0}, but {1} doesn't exist."
SongRequestNumberAndLinkFormat = "#{0} ({1})"
ProcessedSongRequestNumberAndLinkFormat = "#{0} ({1}) [{2} by {3}]"
AutoApproveReason = "Request has been auto-approved"
NoSongRequestsMessage = "{0}, user {1} doesn't have any active song requests."
NonExistentSongRequestNumberMessage = "{0}, non-existent request number {1} for target user {2}."
AlreadyProcessedSongRequestMessage = "{0}, {1}'s song request {2} has already been processed."
SongRequestDecisionReasonMessage = "Reason: {0}."
SongRequestAddedMessage = "{0}, your song request {1} was added and will be processed later."
SongRequestToApproveMessage = "There is a new song request {0} by {1}. Please, approve ({2}) or reject ({3}) it."
SongRequestApprovedMessage = "{0}, your song request {1} was approved by {2} and will be added to playlist later."
OnSuccessSongRequestMessage = "{0}, your song request {1} was added to playlist! Result: {2}."
OnSuccessSongRequestDefaultResultMessage = "Done"
OnFailureSongRequestMessage = "{0}, your song request {1} cannot be added. Error: {2}."
OnFailureSongRequestDefaultErrorMessage = "Unknown error occurred"
SongRequestRejectedMessage = "{0}, your song request {1} was rejected by {2}."
SongRequestDefaultRejectReason = "song didn't pass moderation"
SongRequestCancelMessage = "{0}, your song request {1} was canceled."
GotUserSongRequestsMessage = "{0} has {1} song request(-s): {2}"
NoUserSongRequestsMessage = "{0} has no song requests."
ResetUserSongRequestOptionsMessage = "{0}, {1} reseted your number of ordered requests."
InvalidOptionsSubcommandMessage = "{0}, failed to process unknown subcommand {1}."
FailedToValidateLinkMessage = "{0}, failed to validate your link: {1}"
CommandProcessingDisabledMessage = "{0}, command processing is disabled for this script."
SkipAllSongRequestsMessage = "{0}, all song requests were skipped."
SkipCurrentSongRequestMessage = "{0}, current song requests was skipped."
NoSongRequestsToSkipMessage = "No songs in playlist available to skip."
FailedToSkipSongRequestsMessage = "{0}, failed to skip song requests: {1}"

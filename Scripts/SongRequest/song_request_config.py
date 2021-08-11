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

CommandAddSongRequestUsage = "{0} {1}"
CommandApproveRejectSongRequestUsage = "{0} {1} [{2}]"
ExampleUserIdOrName = "[UserIdOrName]"
ExampleRequestNumberValidRange = "[1–{0}]"
ExampleYouTubeLinkToSong = "[YouTube link]"

EnableWebDriverDebug = False

BrowserDriverPath = "C:\\Program Files\\Common Files\\Webdrivers"
BrowserDriverExecutableName = "MicrosoftWebDriver.exe"

EdgeDriver = "Edge"
ChromeDriver = "Chromium/Chrome"
FirefoxDriver = "Firefox"
OperaDriver = "Opera"
SelectedBrowserDriver = EdgeDriver
ElementIdOfNewSongTextField = "newSong"
ElementIdOfAddSongButton = "playerAddSong"
ClassNameOfNotificationIcon = "ui-pnotify-icon"
ClassNameOfSuccessNotificationIcon = "brighttheme-icon-success"
ClassNameOfErrorNotificationIcon = "brighttheme-icon-error"
ClassNameOfNotificationDescription = "ui-pnotify-text"

# [Required] Script Information.
ScriptName = "SongRequest Script"
Website = "https://github.com/Vasar007/Streamlabs-Chatbot-Scripts"
Description = "Custom song request script."
Creator = "Vasar007"
Version = "1.0.0"

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
CommandUseWhisperSongRequest = "!sr_whisper"
CommandUseWhisperSongRequestCooldown = 1

HttpPageLinkToParse = ""
MaxNumberOfSongRequestsToAdd = 3
UseWhisperMessagesToControlSongRequests = True
DispatchTimeoutInSeconds = 10
TimeoutToWaitInMilliseconds = 3000

# Values: everyone, moderator, subscriber, user_specific, editor.
PermissionOnAddCancelSongRequest = Subscriber
# This field should only be filled when using the user_specific permission.
PermissionInfoOnAddCancelSongRequest = ""

# Values: everyone, moderator, subscriber, user_specific, editor.
PermissionOnApproveRejectGetSongRequest = Moderator
# This field should only be filled when using the user_specific permission.
PermissionInfoOnApproveRejectGetSongRequest = ""

PermissionDeniedMessage = "Permission denied: You have to be a {0} to use {1} command!"
InvalidCommandCallMessage = "Invalid {0} command call. Usage: {1}"
TimeRemainingMessage = "Command {0} is on cooldown. Time remaining: {1} (seconds)."
OnSuccessSongRequestMessage = "{0}, your song request approved and added!"
OnFailureSongRequestMessage = "{0}, your song request finihsed with error: {1}"

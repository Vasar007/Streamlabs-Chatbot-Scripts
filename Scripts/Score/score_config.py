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
LogFileRelativePath = os.path.join("Services", "Scripts", "Score")
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

CommandCreateScoreUsage = "{0} {1} {2} {3}"
CommandUpdateScoreUsage = "{0} {1} {2} {3}"
ExamplePlayerName = "[PlayerName]"
ExampleScoreValue = "[0–∞]"
ExampleOptionalDescription = "[OptionalDescription enclosed in [] brackets]"

# [Required] Script Information.
ScriptName = "Score Script"
Website = "https://github.com/Vasar007/Streamlabs-Chatbot-Scripts"
Description = "Adds an opportunity to create and update score"
Creator = "Vasar007"
Version = "1.0.1"

# Command settings and responses (caution: some of the response texts are
# overwritten later/not refactored yet).
CommandGetScore = "!score"
CommandCreateScore = "!create_score"
CommandUpdateScore = "!update_score"
CommandResetScore = "!reset_score"
CommandDeleteScore = "!delete_score"

# Values: everyone, moderator, subscriber, user_specific, editor.
PermissionOnGet = Everyone
# This field should only be filled when using the user_specific permission.
PermissionInfoOnGet = ""

PermissionOnEdit = Moderator
# This field should only be filled when using the user_specific permission.
PermissionInfoOnEdit = ""

PermissionDeniedMessage = "Permission denied: You have to be a {0} to use {1} command!"

InvalidCommandCallMessage = "Invalid {0} command call. Usage: {1}"
NoScoreFoundMessage = "No score found."
CurrentScoreMessage = "Current score: {0}"
CreatedScoreMessage = "Created new score: {0}"
RecreatedScoreMessage = "Score has created already, created the new one: {0}"
NothingToUpdateMessage = "No score found, nothing to update."
InvalidScoreValueMessage = "Failed to update score: invalid score value {0}. Try value in range: {1}."
UpdatedScoreMessage = "Updated score: {0}"
NothingToResetMessage = "No score found, nothing to reset."
ResetScoreMessage = "Reset score: {0}"
NothingToDeleteMessage = "No score found, nothing to delete."
DeletedScoreMessage = "Deleted score: {0}"

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

# [Required] Script Information.
ScriptName = "SongRequest Script"
Website = "https://github.com/Vasar007/Streamlabs-Chatbot-Scripts"
Description = "Basic boilerplate script to play with."
Creator = "Vasar007"
Version = "1.0.0"

# Command settings and responses (caution: some of the response texts are
# overwritten later/not refactored yet).
CommandPing = "!ping"
Cooldown = 4

# Values: everyone, moderator, subscriber, user_specific, editor.
Permission = Everyone
# This field should only be filled when using the user_specific permission.
PermissionInfo = ""

PermissionDeniedMessage = "Permission denied: You have to be a {0} to use {1} command!"


InvalidCommandCallMessage = "Invalid {0} command call. Usage: {1}"
ResponseMessage = "Pong!"

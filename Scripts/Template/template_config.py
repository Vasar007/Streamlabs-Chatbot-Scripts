# -*- coding: utf-8 -*-

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
LoggingLevel = "Info"

# [Required] Script Information.
ScriptName = "Boilerplate Script"
Website = "https://github.com/Vasar007/Streamlabs-Chatbot-Scripts"
Description = "Basic boilerplate script to play with."
Creator = "Vasar007"
Version = "1.0.0.0"

# Command settings and responses (caution: some of the response texts are
# overwritten later/not refactored yet).
CommandPing = "!ping"
Cooldown = 4

# Values: everyone, moderator, subscriber, user_specific, editor.
Permission = "everyone"

PermissionDeniedMessage = (
    "Permission denied: You have to be a {0} to use {1} command!"
)

# This field should only be filled when using the user_specific permission.
PermissionInfo = ""

InvalidCommandCallMessage = "Invalid {0} command call. Usage: {1}"
ResponseMessage = "Pong!"

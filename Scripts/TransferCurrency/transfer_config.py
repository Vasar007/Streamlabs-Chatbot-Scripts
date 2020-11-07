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
LogFileRelativePath = os.path.join("Services", "Scripts", "TransferCurrency")
LogFileNameFormat = "{0}.log"
LogFileMaxBytes = 10 * 1024 * 1024  # 10 MB
LogFileBackupCount = 10  # Keep last 10 files alive.

LoggingLevel = "Info"
AllowLoggingToFile = False

SettingsReloadEventName = "settings_reload"

CommandGiveUsage = "{0} {1} {2}"
ExampleUserIdOrName = "[UserIdOrName]"
ExampleAmount = "[1–∞]"

# [Required] Script Information.
ScriptName = "Transfer Currency Script"
Website = "https://github.com/Vasar007/Streamlabs-Chatbot-Scripts"
Description = (
    "Allows viewers to transfer Streamlabs currency between eachother."
)
Creator = "Vasar007"
Version = "0.5.1.0"

# Command settings and responses (caution: some of the response texts are
# overwritten later/not refactored yet).
CommandGive = "!give"

GiveTaxPercent = 10
MinGiveAmount = 10
MaxGiveAmount = 100000

# Values: everyone, moderator, subscriber, user_specific, editor.
Permission = "everyone"

PermissionDeniedMessage = (
    "Permission denied: You have to be a {0} to use {1} command!"
)

# This field should only be filled when using the user_specific permission.
PermissionInfo = ""

InvalidCommandCallMessage = "Invalid {0} command call. Usage: {1}"
SuccessfulTransferMessage = "{0} has successfully transferred {1} {2} to {3}."
NotEnoughFundsMessage = "Sorry {0}, you don't have enough {1}."
InvalidAmountMessage = "Sorry {0}, {1} isn't a valid amount. Please, choose integral amount in range: [{2}–{3}]."
NoTargetMessage = "Sorry {0}, but you didn't say who to send the {1} to."
InvalidTargetMessage = "Sorry {0}, but {1} doesn't exist."
TransferToYourselfMessage = "Sorry {0}, but you cannot transfer {1} to yourself."

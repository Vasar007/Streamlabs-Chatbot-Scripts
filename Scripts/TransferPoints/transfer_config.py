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

# Values: everyone, moderator, subscriber, user_specific, editor.
PermissionOnDefaultVersionCommand = Moderator
# This field should only be filled when using the user_specific permission.
PermissionInfoOnDefaultVersionCommand = ""

CommandTransferUsage = "{0} {1} {2}"
ExampleUserIdOrName = "[UserIdOrName]"
ExampleAmountMinMaxRange = "[{0}–{1}]"
ExampleAmountValidRange = "[1–∞]"
ExampleAmountSetRange = "[0–∞]"

# [Required] Script Information.
ScriptName = "Transfer Points Script"
Website = "https://github.com/Vasar007/Streamlabs-Chatbot-Scripts"
Description = "Allows viewers to transfer Streamlabs points between eachother."
Creator = "Vasar007"
Version = "1.1.0"

# Command settings and responses (caution: some of the response texts are
# overwritten later/not refactored yet).
CommandGive = "!give"
CommandGiveCooldown = 1
CommandAdd = "!add"
CommandAddCooldown = 1
CommandRemove = "!remove"
CommandRemoveCooldown = 1
CommandSet = "!set"
CommandSetCooldown = 1
CommandGetTax = "!get_tax"
CommandGetTaxCooldown = 1

ParameterAll = "all"

GiveTaxPercent = 10
MinGiveAmount = 10
MaxGiveAmount = 100000

AllowToTransferToYourself = False

# Values: everyone, moderator, subscriber, user_specific, editor.
PermissionOnGiveGetTax = Everyone
# This field should only be filled when using the user_specific permission.
PermissionInfoOnGiveGetTax = ""

# Values: everyone, moderator, subscriber, user_specific, editor.
PermissionOnAddRemoveSet = Moderator
# This field should only be filled when using the user_specific permission.
PermissionInfoOnAddRemoveSet = ""

AllowToAddRemoveSetForOtherWithSamePermissionOrHigher = False

PermissionDeniedMessage = "Permission denied: You have to be a {0} to use {1} command!"
OperationDeniedMessage = "Permission denied: cannot use {0} command on {1} which has the same or higher permission!"

InvalidCommandCallMessage = "Invalid {0} command call. Usage: {1}"
SuccessfulTransferMessage = "{0} has successfully transferred {1} {2} to {3} (tax: {4})."
SuccessfulAddingMessage = "{0} has successfully added {1} {2} to {3}."
SuccessfulRemovingMessage = "{0} has successfully removed {1} {2} from {3}."
SuccessfulSettingMessage = "{0} has successfully set {1} {2} for {3}."
NotEnoughFundsToTransferMessage = "Sorry {0}, you don't have enough {1} (you have: {2}, required: {3})."
NotEnoughFundsToRemoveMessage = "Sorry {0}, {1} doesn't have enough {2} ({1} has: {3}, required: {4})."
InvalidAmountMessage = "Sorry {0}, {1} isn't a valid amount. Please, choose integral amount in range: {2}."
NoTargetMessage = "Sorry {0}, but you didn't say who to send the {1} to."
InvalidTargetMessage = "Sorry {0}, but {1} doesn't exist."
DeniedTransferToYourselfMessage = "Sorry {0}, but you cannot transfer {1} to yourself."
CurrentTaxPercentMessage = "Current tax: {0}%"
TimeRemainingMessage = "Command {0} is on cooldown. Time remaining: {1} (seconds)."

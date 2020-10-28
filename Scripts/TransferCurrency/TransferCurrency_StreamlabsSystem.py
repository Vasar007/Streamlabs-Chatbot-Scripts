# -*- coding: utf-8 -*-

# Import Libraries.
import os
import sys
import json
import time
import collections
from pprint import pprint
from shutil import copyfile

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

# Load own modules.
ScriptDir = os.path.dirname(__file__)
LibraryDirName = "Library"
SettingsDirName = "Settings"

# Point at current folder for classes/references.
sys.path.append(ScriptDir)

# Point at lib folder for classes/references.
sys.path.append(os.path.join(ScriptDir, LibraryDirName))

import config
import helpers

# Import Settings class.
from transfer_settings import TransferSettings

sys.path.remove(ScriptDir)
sys.path.remove(os.path.join(ScriptDir, LibraryDirName))

# [Required] Script Information (must be existing in this main file).
ScriptName = config.ScriptName
Website = config.Website
Description = config.Description
Creator = config.Creator
Version = config.Version

# Define Global Variables.
SettingsFile = ""
ScriptSettings = TransferSettings()


def Init():
    """
    [Required] Initialize Data (only called on load).
    """
    # Create Settings Directory.
    directory = os.path.join(ScriptDir, SettingsDirName)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Load settings.
    global SettingsFile
    global ScriptSettings
    SettingsFile = os.path.join(ScriptDir, SettingsDirName, "settings.json")
    ScriptSettings = TransferSettings(Parent, SettingsFile)

    Log("Script successfully initialized.")


def Execute(data):
    """
    [Required] Execute Data/Process messages.
    """
    if not data.IsChatMessage():
        return

    # Check if the propper command is used, the command is not on cooldown and
    # the user has permission to use the command.
    command = data.GetParam(0).lower()
    required_permission = ScriptSettings.Permission
    has_permissions = Parent.HasPermission(
        data.User, required_permission, ScriptSettings.PermissionInfo
    )
    if not has_permissions:
        HandleNoPermission(required_permission)

    # !give
    if command == ScriptSettings.CommandGive:
        ProcessGiveCommand(
            data.User,
            data.GetParam(1),
            ScriptSettings.CurrencyName,
            data.GetParam(2)
        )


def Tick():
    """
    [Required] Tick method (Gets called during every iteration even when there
    is no incoming data).
    """
    return


def Parse(parse_string, userid, username, targetid, targetname, message):
    """
    [Optional] Parse method (Allows you to create your own custom $parameters).
    Here"s where the magic happens, all the strings are sent and processed
    through this function.

    Parent.FUNCTION allows to use functions of the Chatbot and other outside
    APIs (see: https://github.com/AnkhHeart/Streamlabs-Chatbot-Python-Boilerplate/wiki/Parent).
    """
    return parse_string


def ReloadSettings(jsonData):
    """
    [Optional] Reload Settings (called when a user clicks the Save Settings
    button in the Chatbot UI).
    """
    # Execute json reloading here.
    try:
        ScriptSettings.reload()
        ScriptSettings.save(SettingsFile)
        Log("Settings reloaded.")
    except Exception as ex:
        Log("Failed to save or reload settings to file: " + str(ex))


def Unload():
    """
    [Optional] Unload (called when a user reloads their scripts or closes the
    bot/cleanup stuff).
    """
    Log("Script unloaded.")


def ScriptToggled(state):
    """
    [Optional] ScriptToggled (notifies you when a user disables your script or
    enables it).
    """
    return


#############################################
# END: Generic Chatbot functions.
#############################################


def Log(message):
    """
    Log helper (for logging into Script Logs of the Chatbot).
    Note that you need to pass the "Parent" object and use the normal
    "Parent.Log" function if you want to log something inside of a module.
    """
    helpers.log(Parent, str(message))


def HandleNoPermission(required_permission):
    message = str(ScriptSettings.PermissionDenied).format(required_permission)
    Log(message)
    Parent.SendTwitchMessage(message)


def ProcessGiveCommand(user, target, currency_name, amount):
    # Input example: !give Vasar 42
    # Command TargetUserName Amount
    try:
        if target in Parent.GetViewerList():
            amount_int = helpers.safe_cast(amount, int)
            if amount_int is None or amount_int <= 0:
                HandleInvalidAmount(user, amount)
            elif amount_int <= Parent.GetPoints(user):
                HandleTransferCurrency(user, target, currency_name, amount_int)
            else:
                HandleNotEnoughFunds(user, currency_name)
        else:
            if not target:
                HandleNoTarget(user, currency_name)
            else:
                HandleInvalidTarget(user, currency_name)
    except Exception as ex:
        Log("Failed to get score: " + str(ex))


def HandleInvalidAmount(user, amount):
    message = str(ScriptSettings.InvalidAmountMessage).format(user, amount)
    Log(message)
    Parent.SendTwitchMessage(message)


def HandleTransferCurrency(user, target, currency_name, amount_int):
    Parent.RemovePoints(user, amount_int)
    Parent.AddPoints(target, amount_int)
    message = (
        str(ScriptSettings.SuccessfulTransferMessage)
        .format(user, amount_int, currency_name, target)
    )
    Log(message)
    Parent.SendTwitchMessage()


def HandleNotEnoughFunds(user, currency_name):
    message = (
        str(ScriptSettings.NotEnoughFundsMessage)
        .format(user, currency_name)
    )
    Log(message)
    Parent.SendTwitchMessage(message)


def HandleNoTarget(user, currency_name):
    message = (
        str(ScriptSettings.NoTargetMessage)
        .format(user, currency_name)
    )
    Log(message)
    Parent.SendTwitchMessage(message)


def HandleInvalidTarget(user, currency_name):
    message = (
        str(ScriptSettings.InvalidTargetMessage)
        .format(user, currency_name)
    )
    Log(message)
    Parent.SendTwitchMessage(message)

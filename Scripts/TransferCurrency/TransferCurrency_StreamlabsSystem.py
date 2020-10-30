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
SettingsFileName = "settings.json"

# Point at current folder for classes/references.
sys.path.append(ScriptDir)

# Point at lib folder for classes/references.
sys.path.append(os.path.join(ScriptDir, LibraryDirName))

import transfer_config as config
import transfer_helpers as helpers

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
    SettingsFile = os.path.join(ScriptDir, SettingsDirName, SettingsFileName)
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

    # !give
    if command == ScriptSettings.CommandGive:
        required_permission = ScriptSettings.Permission
        has_permissions = Parent.HasPermission(
            data.User, required_permission, ScriptSettings.PermissionInfo
        )

        if has_permissions:
            ProcessGiveCommand(
                data.User,
                data.GetParam(1),
                ScriptSettings.CurrencyName,
                data.GetParam(2)
            )
        else:
            HandleNoPermission(required_permission)


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


def ProcessGiveCommand(userid, targetid, currency_name, amount):
    # Input example: !give Vasar 42
    # Command TargetUserNameOrId Amount
    try:
        if targetid in Parent.GetViewerList():
            amount_int = helpers.safe_cast(amount, int)
            if amount_int is None or amount_int <= 0:
                HandleInvalidAmount(userid, amount)
            elif amount_int <= Parent.GetPoints(userid):
                HandleTransferCurrency(userid, targetid, currency_name, amount_int)
            else:
                HandleNotEnoughFunds(userid, currency_name)
        else:
            if not targetid:
                HandleNoTarget(userid, currency_name)
            else:
                HandleInvalidTarget(userid, targetid)
    except Exception as ex:
        Log("Failed to transfer currency: " + str(ex))


def HandleInvalidAmount(userid, amount):
    message = str(ScriptSettings.InvalidAmountMessage).format(userid, amount)
    Log(message)
    Parent.SendTwitchMessage(message)


def HandleTransferCurrency(userid, targetid, currency_name, amount_int):
    current_user_points = Parent.GetPoints(userid)
    current_target_points = Parent.GetPoints(targetid)
    Log(
        "User {0} has {1} {2} before transfer"
        .format(userid, current_user_points, currency_name)
    )
    Log(
        "User {0} has {1} {2} before transfer"
        .format(target, current_target_points, currency_name)
    )

    Parent.RemovePoints(userid, amount_int)
    Parent.AddPoints(targetid, amount_int)
    message = (
        str(ScriptSettings.SuccessfulTransferMessage)
        .format(userid, amount_int, currency_name, targetid)
    )
    Log(message)
    Parent.SendTwitchMessage(message)

    current_user_points = Parent.GetPoints(userid)
    current_target_points = Parent.GetPoints(targetid)
    Log(
        "User {0} has {1} {2} after transfer"
        .format(userid, current_user_points, currency_name)
    )
    Log(
        "User {0} has {1} {2} after transfer"
        .format(targetid, current_target_points, currency_name)
    )


def HandleNotEnoughFunds(userid, currency_name):
    message = (
        str(ScriptSettings.NotEnoughFundsMessage)
        .format(userid, currency_name)
    )
    Log(message)
    Parent.SendTwitchMessage(message)


def HandleNoTarget(userid, currency_name):
    message = (
        str(ScriptSettings.NoTargetMessage)
        .format(userid, currency_name)
    )
    Log(message)
    Parent.SendTwitchMessage(message)


def HandleInvalidTarget(userid, targetid):
    message = (
        str(ScriptSettings.InvalidTargetMessage)
        .format(userid, targetid)
    )
    Log(message)
    Parent.SendTwitchMessage(message)

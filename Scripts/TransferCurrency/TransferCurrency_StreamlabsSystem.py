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
import transfer_helpers as helpers  # pylint:disable=import-error

# Import Settings class.
from transfer_settings import TransferSettings  # pylint:disable=import-error
from transfer_broker import TransferBroker  # pylint:disable=import-error

sys.path.remove(ScriptDir)
sys.path.remove(os.path.join(ScriptDir, LibraryDirName))


# Have pylint know the parent variable.
if False:  # pylint: disable=using-constant-test
    Parent = Parent  # pylint:disable=undefined-variable
# pylint: enable=invalid-name

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

    helpers.init_logging(Parent, ScriptSettings)
    Logger().info("Script successfully initialized.")


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
            ProcessGiveCommand(data)
        else:
            HandleNoPermission(required_permission, command)


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
        ScriptSettings.reload(jsonData)
        ScriptSettings.save(SettingsFile)
        Logger().info("Settings reloaded.")
    except Exception as ex:
        Logger().exception(
            "Failed to save or reload settings to file: " + str(ex)
        )


def Unload():
    """
    [Optional] Unload (called when a user reloads their scripts or closes the
    bot/cleanup stuff).
    """
    Logger().info("Script unloaded.")


def ScriptToggled(state):
    """
    [Optional] ScriptToggled (notifies you when a user disables your script or
    enables it).
    """
    return


#############################################
# END: Generic Chatbot functions.
#############################################


def Logger():
    return helpers.get_logger()


def HandleNoPermission(required_permission, command):
    message = (
        str(ScriptSettings.PermissionDeniedMessage)
        .format(required_permission, command)
    )
    Logger().info(message)
    Parent.SendTwitchMessage(message)


def ProcessGiveCommand(data):
    # Input example: !give Vasar 42
    # Command TargetUserNameOrId Amount
    try:
        userid = data.User
        targetid = data.GetParam(1)
        amount = data.GetParam(2)
        currency_name = Parent.GetCurrencyName()

        broker = TransferBroker(Parent, ScriptSettings, Logger())
        broker.try_send_transfer(userid, targetid, currency_name, amount)
    except Exception as ex:
        Logger().exception("Failed to transfer currency: " + str(ex))

# -*- coding: utf-8 -*-

# Import Libraries.
import os
import sys
import json

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

import template_config as config
import template_helpers as helpers  # pylint:disable=import-error
# pylint:disable=import-error
from template_parent_wrapper import TemplateParentWrapper as ParentWrapper

# Import your Settings class.
from template_settings import TemplateSettings  # pylint:disable=import-error

sys.path.remove(ScriptDir)
sys.path.remove(os.path.join(ScriptDir, LibraryDirName))


# Have pylint know the parent variable.
if False:  # pylint: disable=using-constant-test
    Parent = Parent  # pylint:disable=undefined-variable
# pylint: enable=invalid-name

# [Required] Script Information.
ScriptName = config.ScriptName
Website = config.Website
Description = config.Description
Creator = config.Creator
Version = config.Version

# Define Global Variables.
ParentHandler = None  # Parent wrapper instance.
SettingsFile = ""
ScriptSettings = TemplateSettings()


def Init():
    """
    [Required] Initialize Data (Only called on load).
    """
    # Create Settings Directory.
    directory = os.path.join(ScriptDir, SettingsDirName)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Initialize Parent object wrapper.
    global ParentHandler
    ParentHandler = ParentWrapper(Parent)

    # Load settings.
    global SettingsFile
    global ScriptSettings
    SettingsFile = os.path.join(ScriptDir, SettingsDirName, SettingsFileName)
    ScriptSettings = TemplateSettings(SettingsFile)
    ScriptSettings.Response = "Overwritten pong! ^_^"

    helpers.init_logging(ParentHandler, ScriptSettings)
    Logger().info("Script successfully initialized.")


def Execute(data):
    """
    [Required] Execute Data/Process messages.
    """
    command = data.GetParam(0).lower()
    if not data.IsChatMessage():
        return

    if command != ScriptSettings.Command:
        return

    is_on_user_cooldown = ParentHandler.is_on_user_cooldown(
        ScriptName, ScriptSettings.Command, data.User
    )

    # Check if the propper command is used, the command is not on cooldown
    # and the user has permission to use the command.
    if is_on_user_cooldown:
        cooldown = ParentHandler.get_user_cooldown_duration(
            ScriptName, ScriptSettings.Command, data.User
        )
        ParentHandler.send_stream_message("Time Remaining " + str(cooldown))
    else:
        required_permission = ScriptSettings.Permission
        has_permission = ParentHandler.has_permission(
            data.User, required_permission, ScriptSettings.PermissionInfo
        )
        if not has_permission:
            HandleNoPermission(required_permission, command)
            return

        ParentHandler.broadcast_ws_event("EVENT_MINE", "{'show':false}")
        # Send your message to chat.
        ParentHandler.send_stream_message(ScriptSettings.Response)
        # Put the command on cooldown.
        ParentHandler.add_user_cooldown(
            ScriptName,
            ScriptSettings.Command,
            data.User,
            ScriptSettings.Cooldown
        )


def Tick():
    """
    [Required] Tick method (Gets called during every iteration even when
    there is no incoming data).
    """
    return


def Parse(parseString, userid, username, targetid, targetname, message):
    """
    [Optional] Parse method (Allows you to create your own custom $parameters).
    Here"s where the magic happens, all the strings are sent and processed
    through this function.

    Parent.FUNCTION allows to use functions of the Chatbot and other outside
    APIs (see: https://github.com/AnkhHeart/Streamlabs-Chatbot-Python-Boilerplate/wiki/Parent).
    """
    if "$myparameter" in parseString:
        return parseString.replace("$myparameter", "I am a cat!")

    return parseString


def ReloadSettings(jsonData):
    """
    [Optional] Reload Settings (Called when a user clicks the Save Settings
    button in the Chatbot UI).
    """
    # Execute json reloading here.
    try:
        ScriptSettings.reload(jsonData)
        ScriptSettings.save(SettingsFile)
    except Exception as ex:
        Logger().exception(
            "Failed to save or reload settings to file: " + str(ex)
        )


def Unload():
    """
    [Optional] Unload (Called when a user reloads their scripts or closes
    the bot/cleanup stuff).
    """
    Logger().info("Script unloaded.")


def ScriptToggled(state):
    """
    [Optional] ScriptToggled (Notifies you when a user disables your script or
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
    ParentHandler.send_stream_message(message)

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

# Point at current folder for classes/references.
sys.path.append(ScriptDir)

# Point at lib folder for classes/references.
sys.path.append(os.path.join(ScriptDir, LibraryDirName))

# Import your Settings class.
from template_settings import TemplateSettings

sys.path.remove(ScriptDir)
sys.path.remove(os.path.join(ScriptDir, LibraryDirName))

# [Required] Script Information.
ScriptName = "Template Script"
Website = "https://www.streamlabs.com"
Description = "Basic boilerplate script to play with"
Creator = "Vasar007"
Version = "1.0.0.0"

# Define Global Variables.
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = TemplateSettings()


def Init():
    """
    [Required] Initialize Data (Only called on load).
    """

    # Create Settings Directory.
    directory = os.path.join(ScriptDir, SettingsDirName)
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Load settings.
    global SettingsFile
    global ScriptSettings
    SettingsFile = os.path.join(ScriptDir, SettingsDirName, "settings.json")
    ScriptSettings = TemplateSettings(Parent, SettingsFile)
    ScriptSettings.Response = "Overwritten pong! ^_^"

    Log("Script successfully initialized.")


def Execute(data):
    """
    [Required] Execute Data/Process messages.
    """
    command = data.GetParam(0).lower()
    if not data.IsChatMessage():
        return

    if not command == ScriptSettings.Command:
        return

    if Parent.IsOnUserCooldown(ScriptName, ScriptSettings.Command, data.User):
        cooldown = Parent.GetUserCooldownDuration(
            ScriptName, ScriptSettings.Command, data.User
        )
        Parent.SendStreamMessage("Time Remaining " + str(cooldown))

    # Check if the propper command is used, the command is not on cooldown
    # and the user has permission to use the command.
    if (not Parent.IsOnUserCooldown(ScriptName, ScriptSettings.Command, data.User)
        and Parent.HasPermission(data.User, ScriptSettings.Permission, ScriptSettings.PermissionInfo)):

        Parent.BroadcastWsEvent("EVENT_MINE","{'show':false}")
        # Send your message to chat.
        Parent.SendStreamMessage(ScriptSettings.Response)
        # Put the command on cooldown.
        Parent.AddUserCooldown(
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
    [Optional] Parse method (Allows you to create your own custom
    $parameters).
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
        ScriptSettings.reload()
        ScriptSettings.save(SettingsFile)
    except Exception as ex:
        Log("Failed to save or reload settings to file: " + str(ex))

def Unload():
    """
    [Optional] Unload (Called when a user reloads their scripts or closes
    the bot/cleanup stuff).
    """
    Log("Script unloaded.")


def ScriptToggled(state):
    """
    [Optional] ScriptToggled (Notifies you when a user disables your script or
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
    Parent.Log(ScriptName, str(message))

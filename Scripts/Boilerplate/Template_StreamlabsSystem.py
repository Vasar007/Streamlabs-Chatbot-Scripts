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

# Point at current folder for classes/references.
sys.path.append(ScriptDir)

# Point at lib folder for classes/references.
sys.path.append(os.path.join(ScriptDir, LibraryDirName))

# Import your Settings class.
from Settings_Module import MySettings

sys.path.remove(ScriptDir)
sys.path.remove(os.path.join(ScriptDir, LibraryDirName))

# [Required] Script Information.
ScriptName = "Template Script"
Website = "https://www.streamlabs.com"
Description = "!test will post a message in chat"
Creator = "AnkhHeart"
Version = "1.0.0.0"

# Define Global Variables.
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = MySettings()

def Init():
    """
    [Required] Initialize Data (Only called on load).
    """

    # Create Settings Directory.
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Load settings.
    global SettingsFile
    global ScriptSettings
    SettingsFile = os.path.join(os.path.dirname(__file__), r"Settings\settings.json")
    ScriptSettings = MySettings(SettingsFile)
    ScriptSettings.Response = "Overwritten pong! ^_^"

def Execute(data):
    """
    [Required] Execute Data/Process messages.
    """
    command = data.GetParam(0).lower()
    if not data.IsChatMessage():
        return

    if (command == ScriptSettings.Command and
        Parent.IsOnUserCooldown(ScriptName, ScriptSettings.Command, data.User)):

        cooldown = Parent.GetUserCooldownDuration(
            ScriptName, ScriptSettings.Command, data.User
        )
        Parent.SendStreamMessage("Time Remaining " + str(cooldown))

    # Check if the propper command is used, the command is not on cooldown
    # and the user has permission to use the command.
    if (command == ScriptSettings.Command and
        not Parent.IsOnUserCooldown(ScriptName, ScriptSettings.Command, data.User)
        and Parent.HasPermission(data.User, ScriptSettings.Permission, ScriptSettings.Info)):

        Parent.BroadcastWsEvent("EVENT_MINE","{'show':false}")
        # Send your message to chat.
        Parent.SendStreamMessage(ScriptSettings.Response)
        # Put the command on cooldown.
        Parent.AddUserCooldown(ScriptName,ScriptSettings.Command,data.User,ScriptSettings.Cooldown)


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
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)
    return


def Unload():
    """
    [Optional] Unload (Called when a user reloads their scripts or closes
    the bot/cleanup stuff).
    """
    return


def ScriptToggled(state):
    """
    [Optional] ScriptToggled (Notifies you when a user disables your script or
    enables it).
    """
    return

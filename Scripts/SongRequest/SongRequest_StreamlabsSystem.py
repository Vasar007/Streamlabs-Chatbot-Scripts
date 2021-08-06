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

import song_request_config as config
import song_request_helpers as helpers  # pylint:disable=import-error
# pylint:disable=import-error
from song_request_parent_wrapper import SongRequestParentWrapper as ParentWrapper
# pylint:disable=import-error
from song_request_data_wrapper import SongRequestDataWrapper as DataWrapper

# pylint:disable=import-error
from song_request_command_wrapper import SongRequestCommandWrapper as CommandWrapper

# Import your Settings class.
from song_request_settings import SongRequestSettings  # pylint:disable=import-error

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
ScriptSettings = SongRequestSettings()


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
    ScriptSettings = SongRequestSettings(SettingsFile)
    ScriptSettings.Response = "Overwritten pong! ^_^"

    helpers.init_logging(ParentHandler, ScriptSettings)
    Logger().info("Script successfully initialized.")


def Execute(data):
    """
    [Required] Execute Data/Process messages.
    """
    try:
        data_wrapper = DataWrapper(data)
        if not data_wrapper.is_chat_message():
            return

        # Check if the propper command is used, the command is not on cooldown
        # and the user has permission to use the command.
        command = data_wrapper.get_param(0).lower()
        parsed_command = TryProcessCommand(command, data_wrapper)

        # Check if it is unknown command.
        if parsed_command.is_unknown_command():
            return

        # Check if it is invalid command call.
        if parsed_command.is_invalid_command_call():
            # If user doesn't have permission, write about it at first.
            if not parsed_command.has_func():
                HandleNoPermission(
                    parsed_command.required_permission, parsed_command.command
                )
                return

            message = (
                ScriptSettings.InvalidCommandCallMessage
                .format(parsed_command.command, parsed_command.usage_example)
            )
            Logger().debug(message)
            ParentHandler.send_stream_message(message)
            return

        # If user doesn't have permission, "func" will be equal to "None".
        if parsed_command.has_func():
            parsed_command.func(data_wrapper)
        else:
            HandleNoPermission(
                parsed_command.required_permission, parsed_command.command
            )
    except Exception as ex:
        Logger().exception(
            "Failed to process message: " + str(ex)
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
    Here's where the magic happens, all the strings are sent and processed
    through this function.

    Parent.FUNCTION allows to use functions of the Chatbot and other outside
    APIs (see: https://github.com/AnkhHeart/Streamlabs-Chatbot-Python-Boilerplate/wiki/Parent).
    """
    if "$myparameter" in parseString:
        return parseString.replace("$myparameter", "I am a cat!")

    return parseString


def ReloadSettings(jsondata):
    """
    [Optional] Reload Settings (Called when a user clicks the Save Settings
    button in the Chatbot UI).
    """
    # Execute json reloading here.
    try:
        ScriptSettings.reload(jsondata)
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
        ScriptSettings.PermissionDeniedMessage
        .format(required_permission, command)
    )
    Logger().info(message)
    ParentHandler.send_stream_message(message)


def GetFuncToProcessIfHasPermission(process_command, user_id,
                                    required_permission, permission_info):
    has_permission = ParentHandler.has_permission(
        user_id, required_permission, permission_info
    )
    return process_command if has_permission else None


def TryProcessCommand(command, data_wrapper):
    func = None
    required_permission = None
    is_valid_call = None
    usage_example = None

    # !ping
    if command == ScriptSettings.CommandPing:
        required_permission = ScriptSettings.Permission
        permission_info = ScriptSettings.PermissionInfo
        func = GetFuncToProcessIfHasPermission(
            ProcessPingCommand,
            data_wrapper.user_id,
            required_permission,
            permission_info
        )
        is_valid_call = True  # Ping command call will always be valid.
        usage_example = ScriptSettings.CommandPing

    return CommandWrapper(
        command, func, required_permission, is_valid_call, usage_example
    )


def ProcessPingCommand(data_wrapper):
    # Input example: !ping
    # Command <Anything>
    is_on_user_cooldown = ParentHandler.is_on_user_cooldown(
        ScriptName, ScriptSettings.CommandPing, data_wrapper.user_id
    )

    if is_on_user_cooldown:
        cooldown = ParentHandler.get_user_cooldown_duration(
            ScriptName, ScriptSettings.CommandPing, data_wrapper.user_id
        )
        ParentHandler.send_stream_message("Time Remaining " + str(cooldown))
    else:
        ParentHandler.broadcast_ws_event("EVENT_MINE", "{'show':false}")
        # Send your message to chat.
        ParentHandler.send_stream_message(ScriptSettings.Response)
        # Put the command on cooldown.
        ParentHandler.add_user_cooldown(
            ScriptName,
            ScriptSettings.CommandPing,
            data_wrapper.user_id,
            ScriptSettings.Cooldown
        )

# -*- coding: utf-8 -*-

# TODO:
# Redirect warnings to logger.
# import warnings
# warnings.warn("Warnings message")

# Import Libraries.
import os
import sys

from functools import wraps

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
# pylint:disable=import-error
from template_data_wrapper import TemplateDataWrapper as DataWrapper

# pylint:disable=import-error
from template_command_wrapper import TemplateCommandWrapper as CommandWrapper

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
    ScriptSettings.ResponseMessage = "Overwritten pong! ^_^"

    helpers.init_logging(ParentHandler, ScriptSettings)
    Logger().info("Script successfully initialized.")


def Execute(data):
    """
    [Required] Execute Data/Process messages.
    """
    try:
        # Check whether script can process message.
        data_wrapper = DataWrapper(data)
        if not CanProcessMessage(data_wrapper):
            return

        # Check if the proper command is used, the command is not on cooldown
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
            parsed_command.func(parsed_command.command, data_wrapper)
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


def Parse(parse_string, userid, username, targetid, targetname, message):
    """
    [Optional] Parse method (Allows you to create your own custom $parameters).
    Here's where the magic happens, all the strings are sent and processed
    through this function.

    ATTENTION! Only service messages will be processed. E.g. messages from bot.
    Example: you create command where bot returns in message $myparameter.
    So, script can replace such parameter with custom text
    ("I am a cat!" in our case). Parameter format completely is up to you.
    """
    if "$myparameter" in parse_string:
        return parse_string.replace("$myparameter", "I am a cat!")

    return parse_string


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


def CanProcessMessage(data_wrapper):
    return data_wrapper.is_chat_message()


def HandleNoPermission(required_permission, command):
    message = (
        ScriptSettings.PermissionDeniedMessage
        .format(required_permission, command)
    )
    Logger().info(message)
    ParentHandler.send_stream_message(message)


def WrapCommand(process_command, command_cooldown):
    @wraps(process_command)
    def ProcessCommandWrapper(command, data_wrapper):
        try:
            is_on_cooldown = ParentHandler.is_on_cooldown(ScriptName, command)
            is_on_user_cooldown = ParentHandler.is_on_user_cooldown(
                ScriptName, command, data_wrapper.user_id
            )

            # Check cooldown.
            if is_on_cooldown:
                cooldown = ParentHandler.get_cooldown_duration(
                    ScriptName, command
                )

                # If command is on cooldown, send message.
                message = (
                    ScriptSettings.TimeRemainingMessage
                    .format(command, cooldown)
                )
                ParentHandler.send_stream_message(message)
            elif is_on_user_cooldown:
                cooldown = ParentHandler.get_user_cooldown_duration(
                    ScriptName, command, data_wrapper.user_id
                )

                # If command is on cooldown for user, send message.
                message = (
                    ScriptSettings.TimeRemainingMessage
                    .format(command, cooldown)
                )
                ParentHandler.send_stream_message(message)
            else:
                # If not, process command.
                process_command(command, data_wrapper)
                # Put the command on cooldown.
                ParentHandler.add_cooldown(
                    ScriptName,
                    command,
                    command_cooldown
                )
        except Exception as ex:
            Logger().exception(
                "Failed to process command {0}: {1}".format(command, str(ex))
            )

    return ProcessCommandWrapper


def GetFuncToProcessIfHasPermission(process_command, command_cooldown, user_id,
                                    required_permission, permission_info):
    has_permission = ParentHandler.has_permission(
        user_id, required_permission, permission_info
    )
    return WrapCommand(process_command, command_cooldown) if has_permission else None


def TryProcessCommand(command, data_wrapper):
    func = None
    required_permission = None
    is_valid_call = None
    usage_example = None

    param_count = data_wrapper.get_param_count()

    # !scripts_info
    if command == config.DefaultVersionCommand:
        required_permission = config.PermissionOnDefaultScriptCommands
        permission_info = config.PermissionInfoOnDefaultScriptCommands
        func = GetFuncToProcessIfHasPermission(
            ProcessScriptsInfoCommand,
            config.DefaultVersionCommandCooldown,
            data_wrapper.user_id,
            required_permission,
            permission_info
        )
        # Version command call can have optional text.
        is_valid_call = param_count >= 1

        usage_example = config.DefaultVersionCommand

    # !template_option
    elif command == config.CommandOption:
        required_permission = config.PermissionOnDefaultScriptCommands
        permission_info = config.PermissionInfoOnDefaultScriptCommands
        func = GetFuncToProcessIfHasPermission(
            ProcessOptionCommand,
            config.CommandOptionCooldown,
            data_wrapper.user_id,
            required_permission,
            permission_info
        )
        # Settings command call cannot have optional text
        # but it will be considered as additional string value for settings.
        is_valid_call = param_count >= 3
        usage_example = (
            config.CommandOptionUsage
            .format(
                config.CommandOption,
                config.ExampleOptionName,
                config.ExampleOptionValue
            )
        )

    # !ping
    elif command == ScriptSettings.CommandPing:
        required_permission = ScriptSettings.PermissionOnPing
        permission_info = ScriptSettings.PermissionInfoOnPing
        func = GetFuncToProcessIfHasPermission(
            ProcessPingCommand,
            ScriptSettings.CommandPingCooldown,
            data_wrapper.user_id,
            required_permission,
            permission_info
        )
        is_valid_call = True  # Ping command call will always be valid.
        usage_example = ScriptSettings.CommandPing

    return CommandWrapper(
        command, func, required_permission, is_valid_call, usage_example
    )


def ProcessScriptsInfoCommand(command, data_wrapper):
    # Input example: !scripts_info <Anything>
    # Command <Anything>
    message = "\"{0}\" by {1}, v{2}".format(ScriptName, Creator, Version)
    ParentHandler.send_stream_message(message)


def ProcessOptionCommand(command, data_wrapper):
    # Input example: !template_option <OptionName> <NewValue>
    # Command OptionName NewOptionValue
    ScriptSettings.update_settings_on_the_fly(
        Logger(), ParentHandler, SettingsFile, data_wrapper
    )


def ProcessPingCommand(command, data_wrapper):
    # Input example: !ping
    # Command <Anything>
    ParentHandler.broadcast_ws_event("EVENT_MINE", "{'show':false}")
    # Send your message to chat.
    ParentHandler.send_stream_message(ScriptSettings.ResponseMessage)

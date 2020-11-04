# -*- coding: utf-8 -*-

# Import Libraries.
import os
import sys

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
# pylint:disable=import-error
from transfer_parent_wrapper import TransferParentWrapper as ParentWrapper

# pylint:disable=import-error
from transfer_command_wrapper import TransferCommandWrapper as CommandWrapper

# Import Settings class.
from transfer_settings import TransferSettings  # pylint:disable=import-error
import transfer_broker  # pylint:disable=import-error

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
ParentHandler = None  # Parent wrapper instance.
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

    # Initialize Parent object wrapper.
    global ParentHandler
    ParentHandler = ParentWrapper(Parent)

    # Load settings.
    global SettingsFile
    global ScriptSettings
    SettingsFile = os.path.join(ScriptDir, SettingsDirName, SettingsFileName)
    ScriptSettings = TransferSettings(SettingsFile)

    helpers.init_logging(ParentHandler, ScriptSettings)
    Logger().info("Script successfully initialized.")


def Execute(data):
    """
    [Required] Execute Data/Process messages.
    """
    try:
        if not data.IsChatMessage():
            return

        # Check if the propper command is used, the command is not on cooldown
        # and the user has permission to use the command.
        command = data.GetParam(0).lower()
        parsed_command = TryProcessCommand(command, data)

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
            parsed_command.func(data)
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
    ParentHandler.send_stream_message(message)


def GetFuncToProcessIfHasPermission(process_command, user_id,
                                    required_permission):
    has_permission = ParentHandler.has_permission(
        user_id,
        required_permission,
        ScriptSettings.PermissionInfo
    )
    return process_command if has_permission else None


def TryProcessCommand(command, data):
    func = None
    required_permission = None
    is_valid_call = None
    usage_example = None

    param_count = data.GetParamCount()

    # !give
    if command == ScriptSettings.CommandGive:
        required_permission = ScriptSettings.Permission
        func = GetFuncToProcessIfHasPermission(
            ProcessGiveCommand, data.User, required_permission
        )
        is_valid_call = param_count == 3
        usage_example = (
            config.CommandGiveUsage
            .format(
                ScriptSettings.CommandGive,
                config.ExampleUserIdOrName,
                config.ExampleAmount
            )
        )

    return CommandWrapper(
        command, func, required_permission, is_valid_call, usage_example
    )


def ProcessGiveCommand(data):
    # Input example: !give Vasar 42
    # Command <@>TargetUserNameOrId Amount
    try:
        request = transfer_broker.create_request_from(data, ParentHandler)
        transfer_broker.handle_request(
            request, ParentHandler, ScriptSettings, Logger()
        )
    except Exception as ex:
        Logger().exception("Failed to transfer currency: " + str(ex))

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

import score_config as config
import score_helpers as helpers  # pylint:disable=import-error
# pylint:disable=import-error
from score_parent_wrapper import ScoreParentWrapper as ParentWrapper
# pylint:disable=import-error
from score_data_wrapper import ScoreDataWrapper as DataWrapper

import score  # pylint:disable=import-error
# pylint:disable=import-error
from score_command_wrapper import ScoreCommandWrapper as CommandWrapper
from score_manager import ScoreManager  # pylint:disable=import-error

# Import Settings class.
from score_settings import ScoreSettings  # pylint:disable=import-error

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
ScriptSettings = ScoreSettings()
Manager = None  # Score manager instance.


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
    ScriptSettings = ScoreSettings(SettingsFile)

    # Initialize global variables.
    global Manager
    Manager = ScoreManager(ScriptSettings)

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
            parsed_command.func(Manager, data_wrapper)
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
    Here's where the magic happens, all the strings are sent and processed
    through this function.

    Parent.FUNCTION allows to use functions of the Chatbot and other outside
    APIs (see: https://github.com/AnkhHeart/Streamlabs-Chatbot-Python-Boilerplate/wiki/Parent).
    """
    return parse_string


def ReloadSettings(jsondata):
    """
    [Optional] Reload Settings (called when a user clicks the Save Settings
    button in the Chatbot UI).
    """
    # Execute json reloading here.
    try:
        ScriptSettings.reload(jsondata)
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

    param_count = data_wrapper.get_param_count()

    # !score
    if command == ScriptSettings.CommandGetScore:
        required_permission = ScriptSettings.PermissionOnGet
        permission_info = ScriptSettings.PermissionInfoOnGet
        func = GetFuncToProcessIfHasPermission(
            ProcessGetCommand,
            data_wrapper.user_id,
            required_permission,
            permission_info
        )
        is_valid_call = True  # Get command call will always be valid.
        usage_example = ScriptSettings.CommandGetScore

    # !create_score
    elif command == ScriptSettings.CommandCreateScore:
        required_permission = ScriptSettings.PermissionOnEdit
        permission_info = ScriptSettings.PermissionInfoOnEdit
        func = GetFuncToProcessIfHasPermission(
            ProcessCreateCommand,
            data_wrapper.user_id,
            required_permission,
            permission_info
        )
        is_valid_call = param_count >= 3
        usage_example = (
            config.CommandCreateScoreUsage
            .format(
                ScriptSettings.CommandCreateScore,
                config.ExamplePlayerName,
                config.ExamplePlayerName,
                config.ExampleOptionalDescription
            )
        )

    # !update_score
    elif command == ScriptSettings.CommandUpdateScore:
        required_permission = ScriptSettings.PermissionOnEdit
        permission_info = ScriptSettings.PermissionInfoOnEdit
        func = GetFuncToProcessIfHasPermission(
            ProcessUpdateCommand,
            data_wrapper.user_id,
            required_permission,
            permission_info
        )
        is_valid_call = param_count >= 3
        usage_example = (
            config.CommandUpdateScoreUsage
            .format(
                ScriptSettings.CommandUpdateScore,
                config.ExampleScoreValue,
                config.ExampleScoreValue,
                config.ExampleOptionalDescription
            )
        )

    # !reset_score
    elif command == ScriptSettings.CommandResetScore:
        required_permission = ScriptSettings.PermissionOnEdit
        permission_info = ScriptSettings.PermissionInfoOnEdit
        func = GetFuncToProcessIfHasPermission(
            ProcessResetCommand,
            data_wrapper.user_id,
            required_permission,
            permission_info
        )
        is_valid_call = param_count == 1
        usage_example = ScriptSettings.CommandResetScore

    # !delete_score
    elif command == ScriptSettings.CommandDeleteScore:
        required_permission = ScriptSettings.PermissionOnEdit
        permission_info = ScriptSettings.PermissionInfoOnEdit
        func = GetFuncToProcessIfHasPermission(
            ProcessReloadCommand,
            data_wrapper.user_id,
            required_permission,
            permission_info
        )
        is_valid_call = param_count == 1
        usage_example = ScriptSettings.CommandDeleteScore

    return CommandWrapper(
        command, func, required_permission, is_valid_call, usage_example
    )


def HandleResult(score_handler, to_debug=False):
    if score_handler.is_valid:
        if to_debug:
            Logger().debug(score_handler.message)
        else:
            Logger().info(score_handler.message)
    else:
        Logger().error(score_handler.message)

    ParentHandler.send_stream_message(score_handler.message)


def TryExtractDescription(required_parameters_number, data_wrapper):
    description = ""
    param_count = data_wrapper.get_param_count()
    if param_count > required_parameters_number:
        description = " ".join(
            data_wrapper.get_param(i) 
            for i in range(required_parameters_number, param_count)
        )

    Logger().debug("Extracted description: " + description)
    return description


def ProcessGetCommand(manager, data_wrapper):
    # Input example: !score
    # Command <Anything>
    try:
        score_handler = manager.get_score()
        HandleResult(score_handler, to_debug=True)
    except Exception as ex:
        Logger().exception("Failed to get score: " + str(ex))


def ProcessCreateCommand(manager, data_wrapper):
    # Input example: !create_score Player1 Player2 Score is great!
    # Command Player1Name Player2Name <OptionalDescription>
    try:
        player1_name = data_wrapper.get_param(1)
        player2_name = data_wrapper.get_param(2)
        description = TryExtractDescription(3, data_wrapper)

        score_handler = manager.create_score(
            player1_name, player2_name, description
        )
        HandleResult(score_handler)
    except Exception as ex:
        Logger().exception("Failed to create score: " + str(ex))


def ProcessUpdateCommand(manager, data_wrapper):
    # Input example: !update_score 1 1 Score is great!
    # Command Player1Score Player2Score <OptionalDescription>
    try:
        raw_player1_score = data_wrapper.get_param(1)
        raw_player2_score = data_wrapper.get_param(2)
        description = TryExtractDescription(3, data_wrapper)

        score_handler = manager.update_score(
            raw_player1_score, raw_player2_score, description
        )
        HandleResult(score_handler)
    except Exception as ex:
        Logger().exception("Failed to update score: " + str(ex))


def ProcessResetCommand(manager, data_wrapper):
    # Input example: !reset_score
    # Command
    try:
        score_handler = manager.reset_score()
        HandleResult(score_handler)
    except Exception as ex:
        Logger().exception("Failed to reset score: " + str(ex))


def ProcessReloadCommand(manager, data_wrapper):
    # Input example: !delete_score
    # Command
    try:
        score_handler = manager.delete_score()
        HandleResult(score_handler)
    except Exception as ex:
        Logger().exception("Failed to delete score: " + str(ex))

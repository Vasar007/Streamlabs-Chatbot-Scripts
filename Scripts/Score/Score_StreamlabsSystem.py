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

import score  # pylint:disable=import-error
# pylint:disable=import-error
from score_command_wrapper import ScoreCommandWrapper
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
    if not data.IsChatMessage():
        return

    # Check if the propper command is used, the command is not on cooldown and
    # the user has permission to use the command.
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
        ParentHandler.send_stream_message(message)
        return

    # If user doesn't have permission, "func" will be equal to "None".
    if parsed_command.has_func():
        parsed_command.func(Manager, data)
    else:
        HandleNoPermission(
            parsed_command.required_permission, parsed_command.command
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


def TryProcessCommand(command, data):
    func = None
    required_permission = None
    is_valid_call = None
    usage_example = None

    param_count = data.GetParamCount()

    # !score
    if command == ScriptSettings.CommandGetScore:
        required_permission = ScriptSettings.PermissionOnGet
        func = GetFuncToProcessIfHasPermission(
            ProcessGetCommand, data.User, required_permission
        )
        is_valid_call = True  # Get command call will always be valid.
        usage_example = ScriptSettings.CommandGetScore

    # !new_score
    elif command == ScriptSettings.CommandNewScore:
        required_permission = ScriptSettings.PermissionOnEdit
        func = GetFuncToProcessIfHasPermission(
            ProcessNewCommand, data.User, required_permission
        )
        is_valid_call = param_count == 3
        usage_example = (
            config.CommandNewScoreUsage
            .format(
                ScriptSettings.CommandNewScore,
                config.ExamplePlayerName,
                config.ExamplePlayerName
            )
        )

    # !update_score
    elif command == ScriptSettings.CommandUpdateScore:
        required_permission = ScriptSettings.PermissionOnEdit
        func = GetFuncToProcessIfHasPermission(
            ProcessUpdateCommand, data.User, required_permission
        )
        is_valid_call = param_count == 3
        usage_example = (
            config.CommandUpdateScoreUsage
            .format(
                ScriptSettings.CommandUpdateScore,
                config.ExamplePlayerId,
                config.ExampleScoreValue
            )
        )

    # !reset_score
    elif command == ScriptSettings.CommandResetScore:
        required_permission = ScriptSettings.PermissionOnEdit
        func = GetFuncToProcessIfHasPermission(
            ProcessResetCommand, data.User, required_permission
        )
        is_valid_call = param_count == 1
        usage_example = ScriptSettings.CommandResetScore

    # !delete_score
    elif command == ScriptSettings.CommandDeleteScore:
        required_permission = ScriptSettings.PermissionOnEdit
        func = GetFuncToProcessIfHasPermission(
            ProcessReloadCommand, data.User, required_permission
        )
        is_valid_call = param_count == 1
        usage_example = ScriptSettings.CommandDeleteScore

    return ScoreCommandWrapper(
        command, func, required_permission, is_valid_call, usage_example
    )


def GetFuncToProcessIfHasPermission(process_command, user_id,
                                    required_permission):
    has_permission = ParentHandler.has_permission(
        user_id,
        required_permission,
        ScriptSettings.PermissionInfo
    )
    return process_command if has_permission else None


def HandleResult(score_handler, to_debug=False):
    if score_handler.is_valid:
        if to_debug:
            Logger().debug(score_handler.message)
        else:
            Logger().info(score_handler.message)
    else:
        Logger().error(score_handler.message)

    ParentHandler.send_stream_message(score_handler.message)


def ProcessGetCommand(manager, data):
    # Input example: !score
    # Command
    try:
        score_handler = manager.get_score()
        HandleResult(score_handler)
    except Exception as ex:
        Logger().exception("Failed to get score: " + str(ex))


def ProcessNewCommand(manager, data):
    # Input example: !new_score Player1 Player2
    # Command Player1Name Player2Name
    try:
        player1_name = data.GetParam(1)
        player2_name = data.GetParam(2)

        score_handler = manager.create_score(player1_name, player2_name)
        HandleResult(score_handler)
    except Exception as ex:
        Logger().exception("Failed to create score: " + str(ex))


def ProcessUpdateCommand(manager, data):
    # Input example: !update_score 1 1
    # Command PlayerId NewValue
    try:
        raw_player_id = data.GetParam(1)
        raw_new_score = data.GetParam(2)

        score_handler = manager.update_score(raw_player_id, raw_new_score)
        HandleResult(score_handler)
    except Exception as ex:
        Logger().excpetion("Failed to update score: " + str(ex))


def ProcessResetCommand(manager, data):
    # Input example: !reset_score
    # Command
    try:
        score_handler = manager.reset_score()
        HandleResult(score_handler)
    except Exception as ex:
        Logger().exception("Failed to reset score: " + str(ex))


def ProcessReloadCommand(manager, data):
    # Input example: !delete_score
    # Command
    try:
        score_handler = manager.delete_score()
        HandleResult(score_handler)
    except Exception as ex:
        Logger().exception("Failed to delete score: " + str(ex))

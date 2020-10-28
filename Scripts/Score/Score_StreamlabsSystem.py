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

# Point at current folder for classes/references.
sys.path.append(ScriptDir)

# Point at lib folder for classes/references.
sys.path.append(os.path.join(ScriptDir, LibraryDirName))

import score_config as config
import score_helpers as helpers

import score
from score import Score
from score_command_wrapper import ScoreCommandWrapper

# Import Settings class.
from score_settings import ScoreSettings

sys.path.remove(ScriptDir)
sys.path.remove(os.path.join(ScriptDir, LibraryDirName))

# [Required] Script Information (must be existing in this main file).
# TODO: Some stuff from here should be moved to a GUI settings file later.
ScriptName = config.ScriptName
Website = config.Website
Description = config.Description
Creator = config.Creator
Version = config.Version

# Define Global Variables.
SettingsFile = ""
ScriptSettings = ScoreSettings()
ScoreStorage = {0: None}  # Player1 1:0 Player2


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
    SettingsFile = os.path.join(ScriptDir, SettingsDirName, "settings.json")
    ScriptSettings = ScoreSettings(Parent, SettingsFile)

    # Generate data and archive directory if they don't exist (uses
    # "ScoreDataBackupPath" because it includes the data path).
    if not os.path.isdir(config.ScoreDataBackupPath):
        os.makedirs(config.ScoreDataBackupPath)

    # Creates an empty data file if it doesn't exist.
    if not os.path.isfile(config.ScoreDataFilepath):
        # Generate empty data file and save it.
        helpers.create_json(config.ScoreDataFilepath)

    Log("Script successfully initialized.")


def Execute(data):
    """
    [Required] Execute Data/Process messages.
    """
    if not data.IsChatMessage():
        return

    global ScoreStorage

    # Check if the propper command is used, the command is not on cooldown and
    # the user has permission to use the command.
    command = data.GetParam(0).lower()
    parsed_command = TryProcessCommand(command, data.User)

    # Unknown command.
    if parsed_command.is_unknown_command():
        return

    # If user doesn't have permission, "func" will be equal to "None".
    if parsed_command.has_func():
        ScoreStorage = parsed_command.func(ScoreStorage, data)
    else:
        HandleNoPermission(parsed_command.required_permission)


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
    helpers.backup_data_file()
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


def UpdateDataFile(username):
    """
    UpdateDataFile: Function for modifying the file which contains the data,
    see data/scoredata.json.

    Returns the parse string for parse(Function).
    """
    # currentday = helpers.get_current_day_formatted_date()
    response = "error"

    # This loads the data of file vipdata.json into variable "data".
    datafile = helpers.get_json(config.ScoreDataFilepath)
    response = "NotImplemented"

    # After everything was modified and updated, we need to write the stuff
    # from our "data" variable to the "scoredata.json" file.
    os.remove(config.ScoreDataFilepath)
    helpers.save_json(datafile, config.ScoreDataFilepath)

    return response


def FixDatafileAfterReconnect():
    """
    Fixes data file after reconnect.
    """
    Log("Reconnected, reload saved data.")
    return config.ResponseReloadScore


def TryProcessCommand(command, user):
    func = None
    required_permission = None

    # !score
    if command == ScriptSettings.CommandGetScore:
        required_permission = ScriptSettings.PermissionOnGet
        func = GetFuncToProcessIfHasPermission(
            ProcessGetCommand, user, required_permission
        )

    # !new_score
    elif command == ScriptSettings.CommandNewScore:
        required_permission = ScriptSettings.PermissionOnEdit
        func = GetFuncToProcessIfHasPermission(
            ProcessNewCommand, user, required_permission
        )

    # !update_score
    elif command == ScriptSettings.CommandUpdateScore:
        required_permission = ScriptSettings.PermissionOnEdit
        func = GetFuncToProcessIfHasPermission(
            ProcessUpdateCommand, user, required_permission
        )

    # !reset_score
    elif command == ScriptSettings.CommandResetScore:
        required_permission = ScriptSettings.PermissionOnEdit
        func = GetFuncToProcessIfHasPermission(
            ProcessResetCommand, user, required_permission
        )

    # !reload_score
    elif command == ScriptSettings.CommandReloadScore:
        required_permission = ScriptSettings.PermissionOnEdit
        func = GetFuncToProcessIfHasPermission(
            ProcessReloadCommand, user, required_permission
        )

    return ScoreCommandWrapper(command, func, required_permission)


def GetFuncToProcessIfHasPermission(process_command, user,
                                    required_permission):
    has_permissions = Parent.HasPermission(
        user,
        required_permission,
        ScriptSettings.PermissionInfo
    )
    return process_command if has_permissions else None


def HandleNoPermission(required_permission):
    message = str(ScriptSettings.PermissionDenied).format(required_permission)
    Log(message)
    Parent.SendTwitchMessage(message)


def ProcessGetCommand(score_storage, data):
    try:
        if not score_storage:
            Parent.SendStreamMessage("No score found.")
        else:
            current_score = score_storage[0]
            if current_score is None:
                Parent.SendStreamMessage("No score found.")
            else:
                Parent.SendStreamMessage("Current score " + str(current_score))

        return score_storage
    except Exception as ex:
        Log("Failed to get score: " + str(ex))


def ProcessNewCommand(score_storage, data):
    # Input example: !new_score Player1 Player2
    # Command Player1Name Player2Name
    try:
        new_score = score.create_score_from_string(
            Parent, data.GetParam(1), data.GetParam(2)
        )

        if not score_storage:
            score_storage = {0: new_score}
            Parent.SendStreamMessage("Created new score: " + str(new_score))
        else:
            current_score = score_storage[0]
            if current_score is None:
                score_storage[0] = new_score
                Parent.SendStreamMessage(
                    "Created new score: " + str(new_score)
                )
            else:
                score_storage[0] = new_score
                Parent.SendStreamMessage(
                    "Score has created already, created the new one: " +
                    str(new_score)
                )

        return score_storage
    except Exception as ex:
        Log("Failed to create score: " + str(ex))


def ProcessUpdateCommand(score_storage, data):
    # Input example: !update_score 1 1
    # Command PlayerId NewValue
    try:
        if not score_storage:
            Parent.SendStreamMessage("No score found, nothing to update.")
        else:
            current_score = score_storage[0]
            if current_score is None:
                Parent.SendStreamMessage("No score found, nothing to update.")
            else:
                raw_player_id = data.GetParam(1)
                player_id = helpers.safe_cast(raw_player_id, int)
                if player_id is None:
                    Log(
                        "Failed to update score: invalid player ID " +
                        str(raw_player_id)
                    )

                raw_new_score = data.GetParam(2)
                new_score = helpers.safe_cast(raw_new_score, int)
                if new_score is None:
                    Log(
                        "Failed to update score: invalid score value " +
                        str(raw_new_score)
                    )

                current_score.update_by_string(player_id, new_score)
                Parent.SendStreamMessage(
                    "Updated score: " + str(current_score)
                )

        return score_storage
    except Exception as ex:
        Log("Failed to update score: " + str(ex))


def ProcessResetCommand(score_storage, data):
    try:
        if not score_storage:
            Parent.SendStreamMessage("No score found, nothing to reset.")
        else:
            current_score = score_storage[0]
            if current_score is None:
                Parent.SendStreamMessage("No score found, nothing to reset.")
            else:
                current_score.reset()
                Parent.SendStreamMessage(
                    "Resetted score: " + str(current_score)
                )

        return score_storage
    except Exception as ex:
        Log("Failed to reset score: " + str(ex))


def ProcessReloadCommand(score_storage, data):
    try:
        # TODO: implement reload command.
        Log("Reload score command is not implemented.")

        return score_storage
    except Exception as ex:
        Log("Failed to reload score: " + str(ex))

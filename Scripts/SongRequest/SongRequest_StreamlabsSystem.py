# -*- coding: utf-8 -*-

# Import Libraries.
import os
import sys

from functools import wraps
from datetime import datetime, timedelta

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

# Load own modules.
ScriptDir = os.path.dirname(__file__)
AbsoluteScriptDir = os.path.dirname(os.path.realpath(__file__))
ReferencesDirName = "References"
LibraryDirName = "Library"
SettingsDirName = "Settings"
SettingsFileName = "settings.json"

# Point at current folder for classes/references.
sys.path.append(ScriptDir)

# Point at lib folder for classes/references.
sys.path.append(os.path.join(ScriptDir, LibraryDirName))

# Import C# external dll.
clr.AddReferenceToFileAndPath(os.path.join(AbsoluteScriptDir, ReferencesDirName, "Scripts.SongRequest.CSharp.dll"))
from Scripts.SongRequest.CSharp.Web.Scrapper import HttpWebScrapperFactory
from Scripts.SongRequest.CSharp.Models.Requests import SongRequestModel
from Scripts.SongRequest.CSharp.Models.Requests import SongRequestNumber

import song_request_config as config
import song_request_helpers as helpers  # pylint:disable=import-error
# pylint:disable=import-error
from song_request_parent_wrapper import SongRequestParentWrapper as ParentWrapper
# pylint:disable=import-error
from song_request_data_wrapper import SongRequestDataWrapper as DataWrapper

# pylint:disable=import-error
from song_request_log_wrapper import SongRequestCSharpLogWrapper as CSharpLogWrapper
# pylint:disable=import-error
from song_request_settings import SongRequestCSharpSettings as CSharpSettings

# pylint:disable=import-error
from song_request_command_wrapper import SongRequestCommandWrapper as CommandWrapper

import song_request_manager  # pylint:disable=import-error

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
MessengerHandler = None  # Script messenger instance.
PageScrapper = None  # Song request page scrapper instance.
Manager = None  # Song request manager instance.
LastDispatchTime = datetime.utcnow()
DidPageOpenned = False


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

    # Initialize global variables.
    helpers.init_logging(ParentHandler, ScriptSettings)

    global PageScrapper
    PageScrapper = HttpWebScrapperFactory.Create(
        CSharpSettings(ScriptSettings),
        CSharpLogWrapper(Logger())
    )

    global Manager
    Manager = song_request_manager.create_manager(
        ParentHandler, ScriptSettings, Logger(), PageScrapper
    )

    Logger().info("Script successfully initialized.")


def Execute(data):
    """
    [Required] Execute Data/Process messages.
    """
    try:
        # Script accepts all messages.
        data_wrapper = DataWrapper(data)

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
    global LastDispatchTime
    global DidPageOpenned

    current_time = datetime.utcnow()
    delta = timedelta(seconds=ScriptSettings.DispatchTimeoutInSeconds)

    if current_time < (LastDispatchTime + delta):
        return

    LastDispatchTime = current_time

    if not DidPageOpenned:
        DidPageOpenned = True
        PageScrapper.OpenUrl()

    Manager.run_dispatch()


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
    [Optional] Reload Settings (Called when a user clicks the Save Settings
    button in the Chatbot UI).
    """
    # Execute json reloading here.
    try:
        ScriptSettings.reload(jsondata)
        ScriptSettings.save(SettingsFile)

        PageScrapper.OpenUrl()
    except Exception as ex:
        Logger().exception(
            "Failed to save or reload settings to file: " + str(ex)
        )


def Unload():
    """
    [Optional] Unload (Called when a user reloads their scripts or closes
    the bot/cleanup stuff).
    """
    try:
        if PageScrapper:
            PageScrapper.Dispose()

        Logger().info("Script unloaded.")
    except Exception as ex:
        Logger().exception(
            "Failed to unload script: " + str(ex)
        )


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

    # !sr
    if command == ScriptSettings.CommandAddSongRequest:
        required_permission = ScriptSettings.PermissionOnAddCancelSongRequest
        permission_info = ScriptSettings.PermissionInfoOnAddCancelSongRequest
        func = GetFuncToProcessIfHasPermission(
            ProcessAddSongRequestCommand,
            ScriptSettings.CommandAddSongRequestCooldown,
            data_wrapper.user_id,
            required_permission,
            permission_info
        )
        # Add command call can have optional text.
        is_valid_call = param_count >= 2

        usage_example = (
            config.CommandAddGetSongRequestUsage
            .format(
                ScriptSettings.CommandAddSongRequest,
                config.ExampleYouTubeLinkToSong
            )
        )

    # !sr_approve
    elif command == ScriptSettings.CommandApproveSongRequest:
        required_permission = ScriptSettings.PermissionOnManageSongRequest
        permission_info = ScriptSettings.PermissionInfoOnManageSongRequest
        func = GetFuncToProcessIfHasPermission(
            ProcessApproveRejectSongRequestCommand,
            ScriptSettings.CommandApproveSongRequestCooldown,
            data_wrapper.user_id,
            required_permission,
            permission_info
        )
        # Approve command call can have optional text.
        is_valid_call = param_count >= 2

        usage_example = (
            config.CommandManageSongRequestUsage
            .format(
                ScriptSettings.CommandApproveSongRequest,
                config.ExampleUserIdOrName,
                GetRequestNumberRange()
            )
        )

    # !sr_reject
    elif command == ScriptSettings.CommandRejectSongRequest:
        required_permission = ScriptSettings.PermissionOnManageSongRequest
        permission_info = ScriptSettings.PermissionInfoOnManageSongRequest
        func = GetFuncToProcessIfHasPermission(
            ProcessApproveRejectSongRequestCommand,
            ScriptSettings.CommandRejectSongRequestCooldown,
            data_wrapper.user_id,
            required_permission,
            permission_info
        )
        # Reject command call can have optional reason.
        is_valid_call = param_count >= 2

        usage_example = (
            config.CommandManageSongRequestUsage
            .format(
                ScriptSettings.CommandRejectSongRequest,
                config.ExampleUserIdOrName,
                GetRequestNumberRange()
            )
        )

    # !sr_get
    elif command == ScriptSettings.CommandGetSongRequest:
        required_permission = ScriptSettings.PermissionOnManageSongRequest
        permission_info = ScriptSettings.PermissionInfoOnManageSongRequest
        func = GetFuncToProcessIfHasPermission(
            ProcessGetSongRequestsCommand,
            ScriptSettings.CommandGetSongRequestCooldown,
            data_wrapper.user_id,
            required_permission,
            permission_info
        )
        # Get command call can have optional text.
        is_valid_call = param_count >= 2

        usage_example = (
            config.CommandAddGetSongRequestUsage
            .format(
                ScriptSettings.CommandGetSongRequest,
                config.ExampleUserIdOrName
            )
        )

    # !sr_option
    elif command == ScriptSettings.CommandOptionSongRequest:
        required_permission = ScriptSettings.PermissionOnManageSongRequest
        permission_info = ScriptSettings.PermissionInfoOnManageSongRequest
        func = GetFuncToProcessIfHasPermission(
            ProcessOptionSongRequestsCommand,
            ScriptSettings.CommandOptionSongRequestCooldown,
            data_wrapper.user_id,
            required_permission,
            permission_info
        )
        # Settings command call cannot have optional text
        # but it will be considered as additional string value for settings.
        is_valid_call = param_count >= 3

        usage_example = (
            config.CommandManageSongRequestUsage
            .format(
                ScriptSettings.CommandOptionSongRequest,
                config.ExampleOptionName,
                config.ExampleOptionValue
            )
        )

    return CommandWrapper(
        command, func, required_permission, is_valid_call, usage_example
    )


def GetRequestNumberRange():
    return (
        config.ExampleRequestNumberValidRange
        .format(ScriptSettings.MaxNumberOfSongRequestsToAdd)
    )


def ProcessAddSongRequestCommand(command, data_wrapper):
    # Input example: !sr https://www.youtube.com/watch?v=CAEUnn0HNLM <Anything>
    # Command <YouTube link> <Anything>
    song_link = helpers.wrap_http_link(data_wrapper.get_param(1))
    user_data = helpers.wrap_user_data(
        data_wrapper.user_id, data_wrapper.user_name
    )

    Manager.add_request(user_data, song_link)


def ProcessApproveRejectSongRequestCommand(command, data_wrapper):
    # Input example: !sr_approve/!sr_reject Vasar <Anything>
    # Input example: !sr_approve/!sr_reject Vasar all <Anything>
    # Input example: !sr_approve/!sr_reject Vasar 3 <Anything>
    # Command <@>TargetUserNameOrId <RequestNumber> <Anything>
    song_request_manager.approve_or_reject_request(
        command, data_wrapper, ScriptSettings, Manager
    )


def ProcessGetSongRequestsCommand(command, data_wrapper):
    # Input example: !st_get Vasar <Anything>
    # Command <@>TargetUserNameOrId <Anything>
    song_request_manager.get_all_user_requests(
        data_wrapper, ScriptSettings, Logger(), Manager
    )

def ProcessOptionSongRequestsCommand(command, data_wrapper):
    # Input example: !sr_option Vasar <Anything>
    # Command OptionName NewOptionValue
    raw_user_id = data_wrapper.user_id
    option_name = data_wrapper.get_param(1)

    param_count = data_wrapper.get_param_count()

    raw_new_value = ""
    for i in range(2, param_count):
        raw_new_value += " " + data_wrapper.get_param(i)
    raw_new_value = raw_new_value.strip()

    Logger().info(
        "User {0} want to change option {1} to {2}"
        .format(raw_user_id, option_name, raw_new_value)
    )

    message = None
    try:
        previous_value = ScriptSettings.__dict__[option_name]
        new_value = helpers.safe_cast_with_guess(
            raw_new_value, type(previous_value), previous_value
        )

        if previous_value == new_value:
            message = (
                ScriptSettings.OptionValueTheSameMessage
                .format(option_name, previous_value, new_value)
            )
        else:
            ScriptSettings.__dict__[option_name] = new_value
            message = (
                ScriptSettings.OptionValueChangedMessage
                .format(option_name, previous_value, new_value)
            )
    except Exception as ex:
        message = (
            ScriptSettings.FailedToSetOptionMessage
            .format(option_name, str(ex))
        )
        Logger().exception(message)

    Logger().info(message)
    Manager.get_messenger().send_message(raw_user_id, message)

# -*- coding: utf-8 -*-

import os
from definitions import ROOT_DIR


# [Required] Script Information.
# TODO: Some stuff from here should be moved to a GUI settings file later.
ScriptName = "Score Script"
Website = "https://github.com/Vasar007/Streamlabs-Chatbot-Scripts"
Description = "Adds an opportunity to create and update score"
Creator = "Vasar007"
Version = "0.0.2"

# Global Variables.
# Some stuff from here should be moved to a GUI settings file later.
ScoreDataFolder = "data"
ScoreDataFilename = "scoredata.json"
ScoreDataFilepath = os.path.join(ROOT_DIR, ScoreDataFolder, ScoreDataFilename)
ScoreDataBackupFolder = "archive"  # Inside data path.
ScoreDataBackupFilePrefix = "scoredata_bak-"
ScoreDataBackupPath = os.path.join(
    ROOT_DIR, ScoreDataFolder, ScoreDataBackupFolder
)

# Command settings and responses (caution: some of the response texts are
# overwritten later / not refactored yet).
CommandGetScore = "!score"
CommandNewScore = "!new_score"
CommandUpdateScore = "!update_score"
CommandResetScore = "!reset_score"
CommandReloadScore = "!reload_score"

# Values: everyone, moderator, subscriber, user_specific, editor
PermissionOnGet = "everyone"
PermissionOnEdit = "moderator"

PermissionDenied = (
    "Permission denied: You have to be a {0} to use this command!"
)

# This field should only be filled when using the user_specific permission.
PermissionInfo = ""

ResponseReloadScore = "Okay, I've reset the score and reload the last one."
ResponseOnlyWhenLive = (
    "ERROR: This command is only available, when the stream is live. Sorry!"
)

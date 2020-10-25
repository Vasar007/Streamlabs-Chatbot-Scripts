# -*- coding: utf-8 -*-

import os
from definitions import ROOT_DIR

#---------------------------
#   [Required] Script Information.
#   TODO: Some stuff from here should be moved to a GUI settings file later.
#---------------------------
ScriptName = "Score Script"
Website = "https://github.com/Vasar007/Streamlabs-Chatbot-Scripts"
Description = "Adds an opportunity to create and update score"
Creator = "Vasar007"
Version = "0.0.1-dev"

#---------------------------
#   Global Variables.
#   Some stuff from here should be moved to a GUI settings file later.
#---------------------------
ScoreDataFolder = "data"
ScoreDataFilename = "scoredata.json"
ScoreDataFilepath = os.path.join(ROOT_DIR, ScoreDataFolder, ScoreDataFilename)
ScoreDataBackupFolder = "archive"  # inside data path
ScoreDataBackupFilePrefix = "scoredata_bak-"
ScoreDataBackupPath = os.path.join(ROOT_DIR, ScoreDataFolder, ScoreDataBackupFolder)

#---------------------------
#   Command settings and responses (caution: some of the response texts are overwritten later / not refactored yet).
#---------------------------
Permission = "moderator"

CommandGetScore = "!score"
CommandNewScore = "!new_score"
CommandUpdateScore = "!update_score"
CommandResetScore = "!reset_score"
CommandReloadScore = "!reload_score"

ResponseReloadScore = "Okay, I've reset the score and reload the last one."
ResponsePermissionDeniedMod = "Permission denied: You have to be a Moderator to use this command!"
ResponseOnlyWhenLive = "ERROR: This command is only available, when the stream is live. Sorry!"

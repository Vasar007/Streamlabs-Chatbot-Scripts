# -*- coding: utf-8 -*-


# [Required] Script Information.
# TODO: Some stuff from here should be moved to a GUI settings file later.
ScriptName = "Score Script"
Website = "https://github.com/Vasar007/Streamlabs-Chatbot-Scripts"
Description = "Adds an opportunity to create and update score"
Creator = "Vasar007"
Version = "0.0.3"

# Command settings and responses (caution: some of the response texts are
# overwritten later/not refactored yet).
CommandGetScore = "!score"
CommandNewScore = "!new_score"
CommandUpdateScore = "!update_score"
CommandResetScore = "!reset_score"
CommandReloadScore = "!reload_score"

# Values: everyone, moderator, subscriber, user_specific, editor.
PermissionOnGet = "everyone"
PermissionOnEdit = "moderator"

PermissionDeniedMessage = (
    "Permission denied: You have to be a {0} to use {1} command!"
)

# This field should only be filled when using the user_specific permission.
PermissionInfo = ""

InvalidCommandCall = "Invalid {0} command call."

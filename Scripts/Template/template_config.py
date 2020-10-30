# -*- coding: utf-8 -*-


# [Required] Script Information.
ScriptName = "Boilerplate Script"
Website = "https://github.com/Vasar007/Streamlabs-Chatbot-Scripts"
Description = "Basic boilerplate script to play with."
Creator = "Vasar007"
Version = "1.0.0.0"

# Command settings and responses (caution: some of the response texts are
# overwritten later/not refactored yet).
Command = "!ping"
Cooldown = 4
Response = "Pong!"

# Values: everyone, moderator, subscriber, user_specific, editor.
Permission = "everyone"

PermissionDeniedMessage = (
    "Permission denied: You have to be a {0} to use {1} command!"
)

# This field should only be filled when using the user_specific permission.
PermissionInfo = ""

# Score Script

Score script adds score counter between two opponents.

## Available features

- Create score with opponents names.
- Update score with value.
- Reset score.
- Retrieve current score.
- **(Not implemented)** Backup and reload score from local data.

## How to install script

Check common instruction [here](../../README.md#How_to_install_any_script).

## How to use

Script has several commands and options.
Some of them you can configure though SL Chatbot UI.
The other ones you can change directly in script directory config or script file.

In addition, I can mention that all errors will be caught and logged.
So, if bot doesn't send response, check "Logs" or "Errors" tab in SL Chatbot UI.

### !score

- Description: The command to show current score
- Usage: !score
- Permissions: Everyone

### !new_score

- Description: The command to create new score
- Usage: !new_score Player1 Player2
- Permissions: Moderator or higher
- Arguments:
  - Player1: string — the first player name
  - Player1: string — the second player name

### !update_score

- Description: The command to update current score
- Usage: !update_score PlayerId NewValue
- Permissions: Moderator or higher
- Arguments:
  - PlayerId: integer — the player ID (1 for the first player or 2 for the second player)
  - NewValue: integer — new value to set for target player

### !reset_score

- Description: The command to reset current score
- Usage: !reset_score
- Permissions: Moderator or higher

### !reload_score

**This command is not implemented now.**

- Description: The command to reload current score
- Usage: !reload_score
- Permissions: Moderator or higher

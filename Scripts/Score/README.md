# Score Script

Score script adds score counter between two opponents.

Latest version: `1.0.0.0`

## Available features

- Create score with opponents names.
- Update score with value.
- Reset score.
- Retrieve current score.
- Delete current score.

## How to install script

[Download script](https://github.com/Vasar007/Streamlabs-Chatbot-Scripts/raw/main/Releases/Score.zip).

See common instruction [here](../../README.md#how-to-install-any-script).

## How to use

Script has several commands and options to use.
Some of them you can configure though SL Chatbot UI.
The other ones you can change directly in script directory config or script file.

**Note:** prefer to reload script manually if you change any settings because SL Chatbot can skip settings reload for script sometimes!

In addition, notice that all errors will be caught and logged.
So, if bot doesn't send response, check "Logs" or "Errors" tab in SL Chatbot UI.

**Note:** documentation contains default command names and permissions but you can change script settings.

### !score

- Label: Get Command
- Description: The command to show current score
- Usage: !score
- Permissions: Everyone
- Can have optional text: Yes

### !new_score

- Label: New Command
- Description: The command to create new score
- Usage: !new_score Player1 Player2
- Permissions: Moderator or higher
- Can have optional text: No
- Arguments:
  - Player1: string — the first player name
  - Player1: string — the second player name
- Samples:
  - `!new_score Foo Bar`
  - `!new_score USeR BeasT`

### !update_score

- Label: Update Command
- Description: The command to update current score
- Usage: !update_score Player1Score Player2Score
- Permissions: Moderator or higher
- Can have optional text: No
- Arguments:
  - Player1Score: integer — new value to set for player 1 (positive number)
  - Player2Score: integer — new value to set for player 2 (positive number)
- Samples:
  - `!update_score 1 1`
  - `!update_score 2 5`
  - `!update_score 2 0`

### !reset_score

- Label: Reset Command
- Description: The command to reset current score
- Usage: !reset_score
- Permissions: Moderator or higher
- Can have optional text: No

### !delete_score

- Label: Delete Command
- Description: The command to delete current score
- Usage: !delete_score
- Permissions: Moderator or higher
- Can have optional text: nNoo

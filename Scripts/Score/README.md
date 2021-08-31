# Score Script

Score script adds score counter between two opponents.

Documentation for script version: `1.2.0`

## Available features

- Create score with opponents names.
- Update score with value.
- Reset score.
- Retrieve current score.
- Delete current score.
- Append optional score description.
- Setup command cooldowns.

## How to install script

[Download script of latest version](https://github.com/Vasar007/Streamlabs-Chatbot-Scripts/raw/main/Releases/Latest%20versions/Score.zip).

See common instruction [here](../../README.md#how-to-install-any-script).

## How to use

Script has several commands to use.
You can configure almost all script settings though SL Chatbot UI.
The other ones you can change directly in script directory config (`*_config.py`) or script file.

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

### !create_score

- Label: Create Command
- Description: The command to create new score
- Usage: !create_score Player1 Player2
- Permissions: Moderator or higher
- Can have optional text: No (note: all text after required parameters will be converted to description value)
- Arguments:
  - Player1: string — the first player name
  - Player1: string — the second player name
  - Description: string — optional score description
- Samples:
  - `!create_score Foo Bar`
  - `!create_score USeR BeasT`
  - `!create_score USeR BeasT The rest of params will be description`

### !update_score

- Label: Update Command
- Description: The command to update current score
- Usage: !update_score Player1Score Player2Score
- Permissions: Moderator or higher
- Can have optional text: No (note: all text after required parameters will be converted to description value)
- Arguments:
  - Player1Score: integer — new value to set for player 1 (positive number)
  - Player2Score: integer — new value to set for player 2 (positive number)
  - Description: string — optional score description which will replace the current one
- Samples:
  - `!update_score 1 1`
  - `!update_score 2 5`
  - `!update_score 2 0`
  - `!update_score 2 1 The rest of params will be new description`

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
- Can have optional text: No

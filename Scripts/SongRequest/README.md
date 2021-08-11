# Song Request Script

Custom song request script.

Documentation for script version: `1.0.0`

## Available features

- TODO

## How to install script

[Download script of latest version](https://github.com/Vasar007/Streamlabs-Chatbot-Scripts/raw/main/Releases/Latest%20versions/SongRequest.zip).

See common instruction [here](../../README.md#how-to-install-any-script).

## How to use

Script has single command to use.
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

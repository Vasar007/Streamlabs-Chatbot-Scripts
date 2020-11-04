# Transfer Script

Transfer script allows viewers to transfer Streamlabs currency between eachother.

## Available features

- Transfer Streamlabs currency between two users.

## How to install script

[Download script](https://github.com/Vasar007/Streamlabs-Chatbot-Scripts/raw/main/Releases/TransferCurrency.zip).

See common instruction [here](../../README.md#how-to-install-any-script).

## How to use

Script has single command to use.
You can configure almost all script settings though SL Chatbot UI.
The other ones you can change directly in script directory config (`config.py`) or script file.

**Note:** prefer to reload script manually if you change any settings because SL Chatbot can skip settings reload for script sometimes!

In addition, notice that all errors will be caught and logged.
So, if bot doesn't send response, check "Logs" or "Errors" tab in SL Chatbot UI.

**Note:** documentation contains default command names and permissions but you can change script settings.

### !give

- Label: Chat Command
- Description: Command that users will use when they want to transfer currency
- Usage: !give TargetUserNameOrId Amount
- Permissions: Everyone
- Arguments:
  - TargetUserNameOrId: string — the target user name or ID to transfer currency (if name will be specified, script sends additional request to find target user name), `@` symbol at the beginning is allowed
  - Amount: integer — currency amount to transfer (should be greater than 0)
- Samples:
  - `!give Vasar 42`
  - `!give vasar 42`
  - `!give @Vasar 42`
  - `!give Mark 123`
  - `!give John 456`

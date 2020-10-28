# Transfer Script

Transfer script allows viewers to transfer Streamlabs currency between eachother.

## Available features

- Transfer Streamlabs currency between two users.

## How to install script

See common instruction [here](../../README.md#how-to-install-any-script).

## How to use

Script has single command to use.
You can configure almost all script settings though SL Chatbot UI.
The other ones you can change directly in script directory config (`config.py`) or script file.

In addition, notice that all errors will be caught and logged.
So, if bot doesn't send response, check "Logs" or "Errors" tab in SL Chatbot UI.

**Note:** documentation contains default command names and permissions but you can change script settings.

### !give

- Label: Chat Command
- Description: Command that users will use when they want to transfer currency
- Usage: !give UserName Amount
- Permissions: Everyone
- Arguments:
  - UserName: string — the target user name to transfer currency
  - Amount: integer — currency amount to transfer
- Samples:
  - `!give Vasar 42`
  - `!give Maman 999`
  - `!give Demon 666`

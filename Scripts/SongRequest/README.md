# Song Request Script

Extended song request script.

Documentation for script version: `1.3.0`

## Available features

- Add song requests to song queue (script supports only YouTube music);
- Cancel their own song requests;
- Skip ordered songs;
- Get ordered songs for user;
- Moderators can approve or reject song requests. If there are no moderators, song requests will be auto-approved;
- Change script settings on the fly (does not require to reload script);
- Autoinstall webdriver (only Chrome is supported now).

## How to install script

[Download script of latest version](https://github.com/Vasar007/Streamlabs-Chatbot-Scripts/raw/main/Releases/Latest%20versions/SongRequest.zip).

See common instruction [here](../../README.md#how-to-install-any-script).

## How to use

Script has several commands to use.
You can configure almost all script settings though SL Chatbot UI.
The other ones you can change directly in script directory config (`*_config.py`) or script file.

**Note:** prefer to reload script manually if you change any settings because SL Chatbot can skip settings reload for script sometimes!

In addition, notice that all errors will be caught and logged.
So, if bot doesn't send response, check "Logs" or "Errors" tab in SL Chatbot UI.

**Note:** documentation contains default command names and permissions but you can change script settings.

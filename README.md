# Streamlabs-Chatbot-Scripts

This repository contains some useful Streamlabs Chatbot (SL Chatbot) scripts.

## Available scripts

- [Template](Scripts/Template) — basic boilerplate script to play with ([download](https://github.com/Vasar007/Streamlabs-Chatbot-Scripts/raw/main/Releases/Template.zip)).
- [Score](Scripts/Score) — script that adds score counter between two opponents ([download](https://github.com/Vasar007/Streamlabs-Chatbot-Scripts/raw/main/Releases/Score.zip)).
- [TransferCurrency](Scripts/TransferCurrency) — script that allows viewers to transfer Streamlabs currency between eachother ([download](https://github.com/Vasar007/Streamlabs-Chatbot-Scripts/raw/main/Releases/TransferCurrency.zip)).

## How to install any script

1. Download and install [Python 2.7.13 x86](https://www.python.org/ftp/python/2.7.13/python-2.7.13.msi) (x86 recommend by SL Chatbot team). Then go to "Scripts" -> "Settings" and specify Python directory.
2. Download repository. You can download target script from [Releases](Releases) or with download links. In that case, go to the step 4.
3. Go to the target script directory (starting from the root where SCRIPT_StreamlabsSystem is located).
   Example: `Streamlabs-Chatbot-Scripts/Scripts/Score`
4. Create a ZIP archive for target script directory.
5. Open SL Chatbot, go to the "Script" tab, click "Import" and select ZIP archive with script directory.
6. If script will import successfully, you're good to go!
   Otherwise, check "Errors" and "Logs" tabs.

If you're having trouble with loading scripts in the SL Chatbot, see: [Scripts Explained video](youtube.com/watch?v=l3FBpY-0880)

Finally, feel free to [create new Issue](https://github.com/Vasar007/Streamlabs-Chatbot-Scripts/issues/new) or contact me directly (vasar007@yandex.ru) if you have any question or problems.

## How to use

Enable script in your stream and have fun!

Notice that the script settings in SL Chatbot can be buggy so if you cannot change some settings, you can try to change it directly in config file (`config.py` which stores default values).

**Note:** prefer to reload script manually if you change any settings because SL Chatbot can skip settings reload for script sometimes!

## License information

This project is licensed under the terms of the [Apache License 2.0](LICENSE).

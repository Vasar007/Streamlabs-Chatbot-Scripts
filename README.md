# Streamlabs-Chatbot-Scripts

This repository contains some useful Streamlabs Chatbot (SL Chatbot) scripts.

## Available scripts

- [Template](Scripts/Template) — basic boilerplate script to play with.
- [Score](Scripts/Score) — script that adds score counter between two opponents.
- [TransferCurrency](Scripts/TransferCurrency) — script that allows viewers to transfer Streamlabs currency between eachother.

## How to install any script

1. Download repository. You can download target script from [Releases](Releases). In that case, go to the step 4.
2. Go to the target script directory (starting from the root where SCRIPT_StreamlabsSystem is located).
   Example: `Streamlabs-Chatbot-Scripts/Scripts/Score`
3. Create a ZIP archive for target script directory.
4. Open SL Chatbot, go to the "Script" tab, click "Import" and select ZIP archive with script directory.
5. If script will import successfully, you're good to go!
   Otherwise, check "Errors" and "Logs" tabs.

If you're having trouble with loading scripts in the SL Chatbot, see: [Scripts Explained video](youtube.com/watch?v=l3FBpY-0880)

Finally, feel free to [create new Issue](https://github.com/Vasar007/Streamlabs-Chatbot-Scripts/issues/new) or contact me directly (vasar007@yandex.ru) if you have any question or problems.

## How to use

Enable script in your stream and have fun!

Notice that the script settings in SL Chatbot can be buggy so if you cannot change some settings, you can try to change it directly in config file (`config.py` which stores default values).

## License information

This project is licensed under the terms of the [Apache License 2.0](LICENSE).

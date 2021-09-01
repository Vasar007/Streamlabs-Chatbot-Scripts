# -*- coding: utf-8 -*-

import os
import codecs
import json

import score_config as config
import score_helpers as helpers
from score_event_emitter import ScoreEventEmitter as EventEmitter 


class ScoreSettings(object):

    _reload_event = EventEmitter()

    def __init__(self, settingsfile=None, encoding="utf-8"):
        """
        Load in saved settings file if available or else set default values.
        """
        if settingsfile is None:
            self._set_default()
        else:
            try:
                if os.path.isfile(settingsfile):
                    with codecs.open(settingsfile, encoding=encoding,
                                     mode="r") as f:
                        self.__dict__ = json.load(f, encoding=encoding)
                else:
                    self._set_default()
            except Exception as ex:
                helpers.get_logger().exception(
                    "Failed to load setting: " + str(ex)
                )
                self._set_default()

    def reload(self, jsondata, encoding="utf-8"):
        """
        Reload settings from Chatbot user interface by given json data.
        """
        self.__dict__ = json.loads(jsondata, encoding=encoding)

        ScoreSettings._reload_event.emit(
            config.SettingsReloadEventName, self
        )

    def save(self, settingsfile, encoding="utf-8"):
        """
        Save settings contained within to .json and .js settings files.
        """
        helpers.save_json(self.__dict__, settingsfile)

        with codecs.open(settingsfile.replace("json", "js"),
                         encoding=encoding, mode="w+") as f:
            content = (
                "var settings = {0};".format(
                    json.dumps(self.__dict__, encoding=encoding)
                )
            )
            f.write(content)

    @classmethod
    def subscribe_on_reload(cls, reload_callback):
        """
        Allows to add callback on settings reload event.
        Callback should accept single parameter — current settings class.
        """
        cls._reload_event.on(config.SettingsReloadEventName, reload_callback)

    def update_settings_on_the_fly(self, logger, parent_wrapper, settingsfile,
                                   data_wrapper):
        raw_user_id = data_wrapper.user_id
        raw_user_name = data_wrapper.user_name

        option_name = data_wrapper.get_param(1)
        param_count = data_wrapper.get_param_count()

        raw_new_value = ""
        for i in range(2, param_count):
            raw_new_value += " " + data_wrapper.get_param(i)
        raw_new_value = raw_new_value.strip()

        logger.info(
            "User {0} wants to change option {1} to {2}"
            .format(raw_user_id, option_name, raw_new_value)
        )

        message = None
        try:
            previous_value = self.__dict__[option_name]
            previous_value_type = type(previous_value)
            new_value = helpers.safe_cast_with_guess(
                raw_new_value, previous_value_type
            )

            if new_value is None:
                submessage = (
                    self.FailedToSetOptionInvalidTypeMessage
                    .format(previous_value_type)
                )
                message = (
                    self.FailedToSetOptionMessage
                    .format(raw_user_name, option_name, submessage)
                )
            elif previous_value == new_value:
                message = (
                    self.OptionValueTheSameMessage
                    .format(raw_user_name, option_name, previous_value, new_value)
                )
            else:
                self.__dict__[option_name] = new_value
                message = (
                    self.OptionValueChangedMessage
                    .format(raw_user_name, option_name, previous_value, new_value)
                )

            self.save(settingsfile)
            logger.info(message)
        except KeyError as key_error:
            submessage = self.FailedToSetOptionInvalidNameMessage
            message = (
                self.FailedToSetOptionMessage
                .format(raw_user_name, option_name, submessage)
            )
            logger.exception(message)
        except Exception as ex:
            message = (
                self.FailedToSetOptionMessage
                .format(raw_user_name, option_name, str(ex))
            )
            logger.exception(message)

        parent_wrapper.send_stream_message(message)

    def _set_default(self):
        # Commands group.
        self.CommandGetScore = config.CommandGetScore
        self.CommandGetScoreCooldown = config.CommandGetScoreCooldown
        self.CommandCreateScore = config.CommandCreateScore
        self.CommandCreateScoreCooldown = config.CommandCreateScoreCooldown
        self.CommandUpdateScore = config.CommandUpdateScore
        self.CommandUpdateScoreCooldown = config.CommandUpdateScoreCooldown
        self.CommandResetScore = config.CommandResetScore
        self.CommandResetScoreCooldown = config.CommandResetScoreCooldown
        self.CommandDeleteScore = config.CommandDeleteScore
        self.CommandDeleteScoreCooldown = config.CommandDeleteScoreCooldown

        # Permission group.
        self.PermissionOnGet = config.PermissionOnGet
        self.PermissionInfoOnGet = config.PermissionInfoOnGet
        self.PermissionOnEdit = config.PermissionOnEdit
        self.PermissionInfoOnEdit = config.PermissionInfoOnEdit
        self.PermissionDeniedMessage = config.PermissionDeniedMessage

        # Chat Messages group.
        self.InvalidCommandCallMessage = config.InvalidCommandCallMessage
        self.TimeRemainingMessage = config.TimeRemainingMessage
        self.OptionValueTheSameMessage = config.OptionValueTheSameMessage
        self.OptionValueChangedMessage = config.OptionValueChangedMessage
        self.FailedToSetOptionMessage = config.FailedToSetOptionMessage
        self.FailedToSetOptionInvalidTypeMessage = config.FailedToSetOptionInvalidTypeMessage
        self.FailedToSetOptionInvalidNameMessage = config.FailedToSetOptionInvalidNameMessage
        self.NoScoreFoundMessage = config.NoScoreFoundMessage
        self.CurrentScoreMessage = config.CurrentScoreMessage
        self.CreatedScoreMessage = config.CreatedScoreMessage
        self.RecreatedScoreMessage = config.RecreatedScoreMessage
        self.NothingToUpdateMessage = config.NothingToUpdateMessage
        self.InvalidScoreValueMessage = config.InvalidScoreValueMessage
        self.UpdatedScoreMessage = config.UpdatedScoreMessage
        self.NothingToResetMessage = config.NothingToResetMessage
        self.ResetScoreMessage = config.ResetScoreMessage
        self.NothingToDeleteMessage = config.NothingToDeleteMessage
        self.DeletedScoreMessage = config.DeletedScoreMessage

        # Debugging group.
        self.LoggingLevel = config.LoggingLevel
        self.AllowLoggingToFile = config.AllowLoggingToFile

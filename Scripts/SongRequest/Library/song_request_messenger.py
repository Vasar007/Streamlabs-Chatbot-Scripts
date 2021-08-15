# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class BaseSongRequestMessenger(object):

    __metaclass__ = ABCMeta

    def __init__(self, parent_wrapper):
        self.parent_wrapper = parent_wrapper

    @abstractmethod
    def send_message(self, target_user_id, message):
        raise NotImplementedError()

    @abstractmethod
    def send_message_for_group(self, target_user_ids, message):
        raise NotImplementedError()


class PublicSongRequestMessenger(BaseSongRequestMessenger):

    def __init__(self, parent_wrapper):
        super(PublicSongRequestMessenger, self).__init__(parent_wrapper)

    def send_message(self, target_user_id, message):
        self.parent_wrapper.send_stream_message(message)

    def send_message_for_group(self, target_user_ids, message):
        self.send_message(message)


class WhisperSongRequestMessenger(BaseSongRequestMessenger):

    def __init__(self, parent_wrapper):
        super(WhisperSongRequestMessenger, self).__init__(parent_wrapper)

    def send_message(self, target_user_id, message):
        self.parent_wrapper.send_stream_whisper(target_user_id, message)

    def send_message_for_group(self, target_user_ids, message):
        for target_user_id in target_user_ids:
            self.send_message(target_user_id, message)


def create_messenger(parent_wrapper, settings, logger):
    messenger = None
    if settings.UseWhisperMessagesToControlSongRequests:
        logger.info("Creating whisper messenger.")
        messenger = WhisperSongRequestMessenger(parent_wrapper)
    else:
        logger.info("Creating public messenger.")
        messenger = PublicSongRequestMessenger(parent_wrapper)

    return messenger


class SongRequestMessengerHandler(object):

    def __init__(self, parent_wrapper, settings, logger):
        self.parent_wrapper = parent_wrapper
        self.settings = settings
        self.logger = logger
        self.real_messenger = self._create_messenger()

        # Subscribe on settings reload to correctly change messenger type.
        reload_callback = lambda settings: self._on_settings_reload(settings)
        self.settings.subscribe_on_reload(reload_callback)

    def send_message(self, target_user_id, message):
        self.real_messenger.send_message(target_user_id, message)

    def send_message_for_group(self, target_user_ids, message):
        self.real_messenger.send_message_for_group(target_user_ids, message)

    def _create_messenger(self):
        return create_messenger(self.parent_wrapper, self.settings, self.logger)

    def _on_settings_reload(self, new_settings):
        self.settings = new_settings
        self.real_messenger = self._create_messenger()

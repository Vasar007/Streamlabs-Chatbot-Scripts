# -*- coding: utf-8 -*-

import os
import logging
from logging.handlers import RotatingFileHandler

import template_config as config
import template_helpers as helpers


class TemplateScriptLogHandler(logging.Handler):

    def __init__(self, parent_wrapper, settings, log_level=None):
        super(TemplateScriptLogHandler, self).__init__()

        self._parent_wrapper = parent_wrapper
        self._settings = settings

        # Setup script handler for logging.
        # Should be called only at the end of ctor.
        self._setup_logging(log_level)

    def emit(self, record):
        log_entry = self.format(record)
        self._parent_wrapper.log(config.ScriptName, str(log_entry))

    def _setup_logging(self, log_level):
        self._set_log_level(log_level)

        formatter = TemplateLoggerFactory.create_formatter()
        self.setFormatter(formatter)

        reload_callback = lambda settings: self._on_settings_reload(settings)
        self._settings.subscribe_on_reload(reload_callback)

    def _on_settings_reload(self, new_settings):
        self._settings = new_settings
        self._set_log_level()

    def _set_log_level(self, log_level=None):
        if log_level is None:
            log_level = config.LogLevels[self._settings.LoggingLevel]
        self.setLevel(log_level)


class TemplateFileLogWrapper(object):

    def __init__(self, settings, logger, log_level):
        self._settings = settings
        self._logger = logger
        self._enabled = False  # Flag to track log file handler status.

        # Setup file handler for logging.
        # Should be called only at the end of ctor.
        self._setup_logging(log_level)

    def _setup_logging(self, log_level):
        self._update_logging_setup(log_level)

        reload_callback = lambda settings: self._on_settings_reload(settings)
        self._settings.subscribe_on_reload(reload_callback)

    def _enable_logging(self, log_level):
        # If handler has been already added to logger, just return.
        if self._enabled:
            return

        file_log_handler = TemplateLoggerFactory.create_file_log_handler(
            log_level
        )
        self._logger.addHandler(file_log_handler)
        self._enabled = True
        # Save handler to have an opportunity to remove it later.
        self.file_log_handler = file_log_handler

    def _disable_logging(self):
        # If handler has been already removed from logger, just return.
        if not self._enabled:
            return

        self._logger.removeHandler(self.file_log_handler)
        self._enabled = False
        # Remove handler to free file lock.
        self.file_log_handler.close()
        self.file_log_handler = None

    def _update_logging_setup(self, log_level=None):
        if log_level is None:
            log_level = config.LogLevels[self._settings.LoggingLevel]

        if self._settings.AllowLoggingToFile:
            self._enable_logging(log_level)
        else:
            self._disable_logging()

    def _on_settings_reload(self, new_settings):
        self._settings = new_settings
        self._update_logging_setup()


class TemplateLogWrapper(object):
    """
    Log helper (for logging into Script Logs of the Chatbot).
    Note that you need to pass the "Parent" object and use the normal
    "Parent.Log" function if you want to log something inside of a module.
    """

    def __init__(self, parent_wrapper, settings):
        self._parent_wrapper = parent_wrapper
        self._settings = settings
        self._logger = None
        self._script_log_handler = None
        self._file_log_handler_wrapper = None

    def init_logging(self):
        log_level = config.LogLevels[self._settings.LoggingLevel]
        self._logger = logging.getLogger(config.ScriptName)
        self._logger.setLevel(log_level)

        self._setup_script_logging(log_level)
        self._setup_file_logging(log_level)

    def _setup_script_logging(self, log_level):
        self._script_log_handler = TemplateScriptLogHandler(
            self._parent_wrapper, self._settings, log_level
        )

        self._logger.addHandler(self._script_log_handler)

    def _setup_file_logging(self, log_level):
        # Handler wrapper should add handler to logger based on settings.
        self._file_log_handler_wrapper = TemplateFileLogWrapper(
            self._settings, self._logger, log_level
        )


class TemplateLoggerFactory(object):

    Initialized = False

    @classmethod
    def init_logging(cls, parent_wrapper, settings):
        """
        Initializes logging.
        """
        wrapper = TemplateLogWrapper(parent_wrapper, settings)
        wrapper.init_logging()
        cls.Initialized = True

    @classmethod
    def get_logger(cls):
        """
        Returns instance to write logs.
        """
        if not cls.Initialized:
            null_logger = logging.getLogger(config.ScriptName + "_NULL")
            if not null_logger.handlers:
                null_logger.addHandler(logging.NullHandler())
            null_logger.propagate = False
            return null_logger

        return logging.getLogger(config.ScriptName)

    @classmethod
    def create_formatter(cls):
        formatter = logging.Formatter(
            fmt=config.LogFormat,
            datefmt=config.LogDateFormat
        )
        return formatter

    @classmethod
    def create_file_log_handler(cls, log_level, encoding="utf-8"):
        log_file_name = helpers.get_valid_filename(
            config.LogFileNameFormat.format(config.ScriptName)
        )
        log_file_relative_path = os.path.join(
            config.LogFileRelativePath, log_file_name
        )

        handler = RotatingFileHandler(
            filename=log_file_relative_path,
            mode="a",
            maxBytes=config.LogFileMaxBytes,
            backupCount=config.LogFileBackupCount,
            encoding=encoding,
            delay=0
        )
        handler.setLevel(log_level)

        formatter = cls.create_formatter()
        handler.setFormatter(formatter)
        return handler

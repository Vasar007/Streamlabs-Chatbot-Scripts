# -*- coding: utf-8 -*-

import logging

import transfer_config as config  # pylint:disable=import-error


class TransferScriptLogHandler(logging.Handler):

    def __init__(self, Parent, settings):
        super(TransferScriptLogHandler, self).__init__()

        self.Parent = Parent
        self.settings = settings
        # Setup handler for logging.
        # Should be called only at the end of ctor.
        self._setup_logging()

    def emit(self, record):
        log_entry = self.format(record)
        self.Parent.Log(config.ScriptName, str(log_entry))

    def _setup_logging(self):
        reload_callback = lambda settings: self._on_settings_reload(settings)
        self.settings.set_reload_callback(reload_callback)
        self._set_log_level()

        formatter = logging.Formatter(
            fmt=config.LogFormat,
            datefmt=config.LogDateFormat
        )
        self.setFormatter(formatter)

    def _on_settings_reload(self, new_settings):
        self.settings = new_settings
        self._set_log_level()

    def _set_log_level(self):
        log_level = config.LogLevels[self.settings.LoggingLevel]
        self.setLevel(log_level)


class TransferLogWrapper(object):
    """
    Log helper (for logging into Script Logs of the Chatbot).
    Note that you need to pass the "Parent" object and use the normal
    "Parent.Log" function if you want to log something inside of a module.
    """

    def __init__(self, Parent, settings):
        self.Parent = Parent
        self.settings = settings
        self.logger = None

    def init_logging(self):
        log_level = config.LogLevels[self.settings.LoggingLevel]
        self.logger = logging.getLogger(config.ScriptName)
        self.logger.setLevel(log_level)
        handler = TransferScriptLogHandler(self.Parent, self.settings)
        self.logger.addHandler(handler)


class TransferLoggerFactory(object):

    Initialized = False

    @classmethod
    def init_logging(cls, Parent, settings):
        """
        Initializes logging.
        """
        wrapper = TransferLogWrapper(Parent, settings)
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

# -*- coding: utf-8 -*-

import queue_config as config
import queue_helpers as helpers  # pylint:disable=import-error


class QueueManager(object):

    def __init__(self, settings, logger, parent_wrapper):
        self._settings = settings
        self._logger = logger
        self._parent_wrapper = parent_wrapper

    def get_queue_info(self, max_value):
        self._logger.debug(
            "Getting queue info with value {0}.".format(max_value)
        )

        queue_info = self._get_queue_info(max_value)

        formatted_info = self._format_queue_info(queue_info)

        message = self._settings.AllQueueInfoStateMessage.format(formatted_info)

        return message

    def get_queue_info_for_user(self, max_value, user_id_or_name):
        self._logger.debug(
            "Getting queue info for user value {0} with value {1}."
            .format(user_id_or_name, max_value)
        )

        queue_info = self._get_queue_info(max_value)

        user_position = self._get_user_position(queue_info, user_id_or_name)

        message = None
        if user_position is not None:
            message = self._settings.UserIsInQueueMessage.format(
                user_id_or_name, user_position
            )
        else:
            message = self._settings.UserIsNotInQueueMessage.format(
                user_id_or_name
            )

        return message

    def _get_queue_info(self, max_value):
        # Retrieves "max_value" amount of users that are in the
        # queue at the moment.
        # PythonDictionary<int position, string userid>
        return self._parent_wrapper.get_queue(max_value)

    def _format_user_and_position(self, user_id, position):
        return config.DefaultUserInQueueFormat.format(
            position, user_id
        )

    def _format_queue_info(self, queue_info):
        formatted_info = ""
        if queue_info:
            for position, user_id in queue_info.items():
                if formatted_info:
                    formatted_info += "{0} ".format(config.DefaultDelimeter)
                formatted_info += self._format_user_and_position(
                    user_id, position
                )
        else:
            formatted_info = self._settings.QueueIsEmptyMessage

        return formatted_info

    def _get_user_position(self, queue_info, user_id_or_name):
        if queue_info:
            user_id_or_name_lower = user_id_or_name.lower()
            for position, user_id in queue_info.items():
                self._logger.debug(
                    self._format_user_and_position(user_id, position)
                )
                if user_id_or_name_lower == user_id.lower():
                    return position

        return None


def create_manager(parent_wrapper, settings, logger):
    return QueueManager(
        settings,
        logger,
        parent_wrapper
    )


def output_queue_info_for_user(manager, data_wrapper, parent_wrapper, logger,
                               settings):
    user_id_or_name = helpers.strip_at_symbol_for_name(
        data_wrapper.get_param(2)
    )
    max_value = config.DefaultAllValueAsInt

    message = manager.get_queue_info_for_user(max_value, user_id_or_name)

    logger.info(message)
    parent_wrapper.send_stream_message(message)


def output_queue_info(manager, data_wrapper, parent_wrapper, logger, settings):
    count_value = data_wrapper.get_param(1)

    max_value = config.DefaultAllValueAsInt
    if settings.is_all_parameter(count_value):
        max_value = config.DefaultAllValueAsInt
    elif count_value.isdigit():
        max_value = helpers.safe_cast(
            count_value, int, config.DefaultAllValueAsInt
        )
        # Protect from overflow.
        max_value = min(max_value, config.DefaultMaxValue)

    message = manager.get_queue_info(max_value)

    logger.info(message)
    parent_wrapper.send_stream_message(message)

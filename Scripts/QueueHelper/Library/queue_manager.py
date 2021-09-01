# -*- coding: utf-8 -*-


def output_queue_info(data_wrapper, parent_wrapper, logger, settings):
    max_value = 10
    # Retrieves "max_value" amount of users that are in the queue at the moment.
    # PythonDictionary<int position, string userid>
    queue_info = parent_wrapper.get_queue(max_value)

    formatted_info = ""
    if queue_info:
        for position, user_id in queue_info.items():
            if formatted_info:
                formatted_info += ", "
            formatted_info += "#{0} {1}".format(position, user_id)
    else:
        formatted_info = settings.QueueIsEmptyMessage

    message = settings.AllQueueInfoStateMessage.format(formatted_info)

    logger.info(message)
    parent_wrapper.send_stream_message(message)

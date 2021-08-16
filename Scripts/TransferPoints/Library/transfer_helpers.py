# -*- coding: utf-8 -*-

# Contains some helpful miscellaneous functions.

import os
import re
import time
import json
import codecs
from datetime import datetime

from transfer_log_wrapper import TransferLoggerFactory as LoggerFactory


def get_current_day_formatted_date():
    """
    Returns the formatted date of current day.
    """
    current_timestamp = int(time.time())
    return datetime.fromtimestamp(current_timestamp).strftime('%Y-%m-%d')


def get_twitch_api_response(parent_wrapper, url):
    """
    Returns the response from api request.
    """
    headers = {"Accept": "application/vnd.twitchtv.v5+json"}
    return parent_wrapper.get_request(url, headers)


def log_all_variables_of_video_object(parent_wrapper, video_object):
    """
    Helper class to log all variables of last stream object (debugging).
    """
    logger = get_logger()
    for attributes in video_object:
        logger.debug(attributes)


def get_attribute_by_video_list_id(parent_wrapper, attribute, list_id,
                                   api_url_last_stream, api_video_limit):
    """
    Gets stream id of given stream by list id (offset to the current stream).
    """
    last_videos_object_storage = get_twitch_api_response(
        parent_wrapper, api_url_last_stream
    )

    last_video_object = get_video_of_video_object_storage_by_list_id(
        parent_wrapper, last_videos_object_storage, list_id, api_video_limit
    )

    return last_video_object.get(str(attribute))


def get_current_stream_id(parent_wrapper, api, api_url_current_stream):
    """
    Gets stream id of current stream for channel.
    """
    current_stream_object_storage = get_twitch_api_response(
        parent_wrapper, api_url_current_stream
    )

    current_stream_object = get_stream_object_by_object_storage(
        current_stream_object_storage
    )

    return current_stream_object.get("_id")


def get_video_of_video_object_storage_by_list_id(parent_wrapper,
                                                 video_object_storage,
                                                 list_id, api_video_limit):
    """
    hint: listId 0 = current stream.
    """
    list_id = int(list_id)  # Let's be safe here.

    parsed_last_video = json.loads(video_object_storage)

    # str.
    data_response = parsed_last_video["response"]
    # dict, contents: _total, videos.
    parsed_data_response = json.loads(data_response)
    # list.
    videos_list = parsed_data_response.get("videos")

    log = get_logger()
    while (int(videos_list[list_id].get("broadcast_id")) == 1 or
           videos_list[list_id].get("status") == "recording"):

        if (list_id >= int(api_video_limit)):
            message = (
                "Failed to find valid stream object in list of " +
                "defined last videos of channel."
            )
            log.debug(message)
            break

        list_id += 1

    # dict.
    return videos_list[list_id]


def get_stream_object_by_object_storage(stream_object_torage):
    """
    Gets stream object by object storage.
    """
    parsed_stream_object_storage = json.loads(stream_object_torage)
    data_response = parsed_stream_object_storage["response"]  # str.
    parsed_data_response = json.loads(data_response)  # dict.
    return parsed_data_response.get("stream")


def init_logging(parent_wrapper, settings):
    """
    Initializes logging for script.
    """
    LoggerFactory.init_logging(parent_wrapper, settings)


def get_logger():
    """
    Retrieve actual logger or NullLogger if logging is not initialized.
    """
    return LoggerFactory.get_logger()


def get_json(filename, work_dir=None):
    """
    Reads a json file.
    """
    path = filename
    if work_dir is not None:
        path = os.path.join(work_dir, filename)

    with codecs.open(path, encoding="utf-8") as file:
        result = json.load(file, encoding="utf-8")
    return result


def create_json(filename, work_dir=None):
    """
    Creates a new json file.
    """
    path = filename
    if work_dir is not None:
        path = os.path.join(work_dir, filename)

    with codecs.open(path, "w", encoding="utf-8") as file:
        json.dump({}, file, encoding="utf-8")


def save_json(dictionary, filename, work_dir=None):
    """
    Saves data to json.
    """
    path = filename
    if work_dir is not None:
        path = os.path.join(work_dir, filename)

    with codecs.open(path, "w", encoding="utf-8") as file:
        json.dump(
            dictionary, file, encoding="utf-8",
            sort_keys=True, indent=4
        )


def has_command(message, command):
    """
    Checks if the message begins with a command as its own word.
    """
    return re.search(r"^{}\b".format(re.escape(command)), message)


def strip_command(message, command):
    """
    Retrieves message content without the command.
    """
    return message.replace(command, "", 1).strip()


def str_to_bool(value):
    """
    Converts string value to boolean.
    """
    return value.lower() in ("yes", "true", "t", "1")


def safe_cast(val, to_type, default=None):
    """
    Provides safe cast to target type.
    """
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def safe_cast_with_guess(val, target_type, default=None):
    """
    Provides safe cast to target type with predefined type cast function.
    Supported types: int, float, bool, str
    """
    if target_type == int:
        return safe_cast(val, int, default)
    elif target_type == float:
        return safe_cast(val, float, default)
    elif target_type == bool:
        return str_to_bool(val)
    elif target_type == str:
        return safe_cast(val, str, default)
    else:
        raise ValueError("Unknown target type {0} to cast".format(target_type))


def strip_at_symbol_for_name(user_name):
    """
    Retrieves user name without @ symbol at the beginning.
    """
    if not user_name:
        return user_name

    if user_name.startswith("@"):
        return user_name[1:]

    return user_name


def get_valid_filename(raw_filename):
    """
    Filters invalid characters for filename.
    """
    raw_filename = str(raw_filename).strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", raw_filename)


def first_or_default(iterable, default=False, pred=None):
    """
    Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.
    """
    # first_or_default([a, b, c], x) --> a or b or c or x
    # first_or_default([a, b], x, f) --> a if f(a) else b if f(b) else x
    iterable_internal = iter(filter(pred, iterable))
    return next(iterable_internal, default)


def lazy_property(fn):
    """
    Decorator that makes a property lazy-evaluated.
    """
    attr_name = "_lazy_" + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return _lazy_property

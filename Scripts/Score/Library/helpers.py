# -*- coding: utf-8 -*-

#---------------------------
# Contains some helpful miscellaneous functions.
#---------------------------

import os
import re
import time
import json
import codecs
from datetime import datetime
from shutil import copyfile

import config


def get_current_day_formatted_date():
    """
    Returns the formatted date of current day.
    """
    current_timestamp = int(time.time())
    return datetime.fromtimestamp(current_timestamp).strftime('%Y-%m-%d')


def get_twitch_api_response(Parent, url):
    """
    Returns the response from api request.
    """
    headers = {"Accept": "application/vnd.twitchtv.v5+json"}
    return Parent.GetRequest(url, headers)


def log_all_variables_of_video_object(Parent, video_object):
    """
    Helper class to log all variables of last stream object (debugging).
    """
    for attributes in video_object:
        log(Parent, attributes)


def get_attribute_by_video_list_id(Parent, attribute, list_id, api_url_last_stream, api_video_limit):
    """
    Gets stream id of given stream by list id (offset to the current stream).
    """
    last_videos_object_storage = get_twitch_api_response(Parent, api_url_last_stream)
    last_video_object = get_video_of_video_object_storage_by_list_id(Parent, last_videos_object_storage, list_id, api_video_limit)
    return last_video_object.get(str(attribute))


def get_current_stream_id(Parent, api, api_url_current_stream):
    """
    Gets stream id of current stream for channel.
    """
    current_stream_object_storage = get_twitch_api_response(Parent, api_url_current_stream)
    current_stream_object = get_stream_object_by_object_storage(current_stream_object_storage)
    return current_stream_object.get("_id")


def get_video_of_video_object_storage_by_list_id(Parent, video_object_storage, list_id, api_video_limit):
    """
    hint: listId 0 = current stream.
    """
    list_id = int(list_id)  # Let's be safe here.

    parsed_last_video = json.loads(video_object_storage)
    data_response = parsed_last_video["response"]  # str.
    parsed_data_response = json.loads(data_response)  # dict, contents: _total, videos.
    videos_list = parsed_data_response.get("videos")  # list.

    while (int(videos_list[list_id].get("broadcast_id")) == 1 or videos_list[list_id].get("status") == "recording"):
        if (list_id >= int(api_video_limit)):
            log(Parent, "Failed to find valid stream object in list of defined last videos of channel.")
            break

        list_id += 1

    return videos_list[list_id]  # dict.


def get_stream_object_by_object_storage(stream_object_torage):
    """
    Gets stream object by object storage.
    """
    parsed_stream_object_storage = json.loads(stream_object_torage)
    data_response = parsed_stream_object_storage["response"]  # str.
    parsed_data_response = json.loads(data_response)  # dict.
    return parsed_data_response.get("stream")


def log(Parent, message):
    """
    Log helper (for logging into Script Logs of the Chatbot).
    Note that you need to pass the "Parent" object and use the normal "Parent.Log" function if you want to log something inside of a module.
    """
    Parent.Log(config.ScriptName, str(message))


def backup_data_file():
    """
    Backups the data file in the "archive" folder with current date and timestamp for ease of use.
    """
    if os.path.isfile(config.ScoreDataFilepath):
        if not os.path.isdir(config.ScoreDataBackupPath):
            os.makedirs(config.ScoreDataBackupPath)

        dst_filename = config.ScoreDataBackupFilePrefix + str(get_current_day_formatted_date()) + "_" + str(int(time.time())) + ".json"
        dst_filepath = os.path.join(config.ScoreDataBackupPath, dst_filename)
        copyfile(config.ScoreDataFilepath, dst_filepath)


def get_json(filename, work_dir=None):
    """
    Reads a json file.
    """
    path = filename
    if work_dir is not None:
        path = os.path.join(work_dir, filename)

    with codecs.open(path, encoding="utf-8-sig") as file:
        result = json.load(file, encoding="utf-8-sig")
    return result


def create_json(filename, work_dir=None):
    """
    Creates a new json file.
    """
    path = filename
    if work_dir is not None:
        path = os.path.join(work_dir, filename)

    with codecs.open(path, "w", encoding="utf-8-sig") as file:
        json.dump({}, file, encoding="utf-8-sig")


def save_json(dictionary, filename, work_dir=None):
    """
    Saves data to json.
    """
    path = filename
    if work_dir is not None:
        path = os.path.join(work_dir, filename)

    with codecs.open(path, "w", encoding="utf-8-sig") as file:
        json.dump(dictionary, file, encoding="utf-8-sig", sort_keys=True, indent=4)


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
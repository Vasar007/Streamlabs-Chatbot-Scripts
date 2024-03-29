# -*- coding: utf-8 -*-

import logging

from Scripts.SongRequest.CSharp.Core.Models import UserData


class SongRequestUserSearcher(object):

    def __init__(self, parent_wrapper, logger):
        self._parent_wrapper = parent_wrapper
        self._logger = logger

    def find_user_data(self, user_id_or_name):
        if not user_id_or_name:
            self._logger.debug(
                "Invalid argument to find user ID: " + user_id_or_name
            )
            return UserData.Empty

        self._logger.debug(
            "Trying to find user ID for value: " + user_id_or_name
        )

        user_id_or_name_low = user_id_or_name.lower()

        # Retrieve viewers data.
        # List<string userid>
        viewer_ids = self._parent_wrapper.get_viewer_list()
        self._log_viewers(viewer_ids)

        # Try to find target user by original parameter.
        result = self._find_by_supposed_id(user_id_or_name_low, viewer_ids)
        if result.HasValue:
            return result

        # Use another method to retrieve viewers data.
        # List<string userid>
        active_users_ids = self._parent_wrapper.get_active_users()
        self._log_viewers(active_users_ids)

        self._logger.debug(
            "WARNING! Cannot find target user by 'get_viewer_list' request." +
            "Using 'get_active_users' request to find user."
        )
        # Try to find target user by original parameter.
        result = self._find_by_supposed_id(
            user_id_or_name_low, active_users_ids
        )
        if result.HasValue:
            return result

        self._logger.debug(
            "WARNING! Cannot find target user by get_viewer_list request. " +
            "Using dangerous extended search to find user."
        )

        # Retrieve extended viewers data.
        # PythonDictionary<string userid, string username>.
        viewers = self._parent_wrapper.get_display_names(viewer_ids)
        self._log_viewers(viewers)

        self._logger.debug(
            "Quick search failed, need to find among all ({0}) users."
            .format(len(viewers))
        )

        # Finally, try to find target user among all users manually.
        return self._find_among_all_users(user_id_or_name, viewers)

    def _find_by_supposed_id(self, supposed_user_id, viewer_ids):
        if supposed_user_id in viewer_ids:
            supposed_name = self._parent_wrapper.get_display_name(
                supposed_user_id
            )
            result = UserData.Create(supposed_user_id, supposed_name)
            self._logger.debug("Found user data (#1): " + str(result))
            return result

        return UserData.Empty

    def _find_among_all_users(self, user_id_or_name, viewers):
        user_id_or_name_low = user_id_or_name.lower()

        for user_id, user_name in viewers.iteritems():
            if user_id_or_name == user_name:
                result = UserData.Create(user_id, user_name)
                self._logger.debug("Found user data (#2): " + str(result))
                return result
            if user_id_or_name_low == user_name:
                result = UserData.Create(user_id, user_name)
                self._logger.debug("Found user data (#3): " + str(result))
                return result

        self._logger.debug("Cannot find user ID for value: " + user_id_or_name)
        return UserData.Empty

    def _log_viewers(self, viewers):
        if not self._logger.isEnabledFor(logging.DEBUG):
            return

        message = (
            "Retrieved {0} users: [{1}].".format(len(viewers), str(viewers))
        )
        self._logger.debug(message)

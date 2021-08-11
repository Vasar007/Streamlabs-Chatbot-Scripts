# -*- coding: utf-8 -*-

import logging

from transfer_user_data import TransferUserData as UserData


class TransferUserSearcher(object):

    def __init__(self, parent_wrapper, logger):
        self.parent_wrapper = parent_wrapper
        self.logger = logger

    def find_user_data(self, user_id_or_name):
        if not user_id_or_name:
            self.logger.debug(
                "Invalid argument to find user ID: " + user_id_or_name
            )
            return UserData.empty()

        self.logger.debug(
            "Trying to find user ID for value: " + user_id_or_name
        )

        user_id_or_name_low = user_id_or_name.lower()

        # Retrive viewers data.
        # List<string userid>
        viewer_ids = self.parent_wrapper.get_viewer_list()
        self._log_viewers(viewer_ids)

        # Try to find target user by original parameter.
        result = self._find_by_supposed_id(user_id_or_name_low, viewer_ids)
        if result:
            return result

        # Use another method to retrieve viewers data.
        # List<string userid>
        active_users_ids = self.parent_wrapper.get_active_users()
        self._log_viewers(active_users_ids)

        self.logger.debug(
            "WARNING! Cannot find target user by 'get_viewer_list' request." +
            "Using 'get_active_users' request to find user."
        )
        # Try to find target user by original parameter.
        result = self._find_by_supposed_id(
            user_id_or_name_low, active_users_ids
        )
        if result:
            return result

        self.logger.debug(
            "WARNING! Cannot find target user by get_viewer_list request. " +
            "Using dangerous extended search to find user."
        )

        # Retrive extended viewers data.
        # PythonDictionary<string userid, string username>.
        viewers = self.parent_wrapper.get_display_names(viewer_ids)
        self._log_viewers(viewers)

        self.logger.debug(
            "Quick search failed, need to find among all ({0}) users."
            .format(len(viewers))
        )

        # Finally, try to find target user among all users manually.
        return self._find_among_all_users(user_id_or_name, viewers)

    def _find_by_supposed_id(self, supposed_user_id, viewer_ids):
        if supposed_user_id in viewer_ids:
            supposed_name = self.parent_wrapper.get_display_name(
                supposed_user_id
            )
            result = UserData(supposed_user_id, supposed_name)
            self.logger.debug("Found user data (#1): " + str(result))
            return result

        return UserData.empty()

    def _find_among_all_users(self, user_id_or_name, viewers):
        user_id_or_name_low = user_id_or_name.lower()

        for user_id, user_name in viewers.iteritems():
            if user_id_or_name == user_name:
                result = UserData(user_id, user_name)
                self.logger.debug("Found user data (#2): " + str(result))
                return result
            if user_id_or_name_low == user_name:
                result = UserData(user_id, user_name)
                self.logger.debug("Found user data (#3): " + str(result))
                return result

        self.logger.debug("Cannot find user ID for value: " + user_id_or_name)
        return UserData.empty()

    def _log_viewers(self, viewers):
        if not self.logger.isEnabledFor(logging.DEBUG):
            return

        message = (
            "Retrieved {0} users: [{1}].".format(len(viewers), str(viewers))
        )
        self.logger.debug(message)

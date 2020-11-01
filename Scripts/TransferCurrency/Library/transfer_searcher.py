# -*- coding: utf-8 -*-


class TransferUserSearcher(object):

    def __init__(self, Parent, logger):
        self.Parent = Parent
        self.logger = logger

    def find_user_id_and_name(self, user_id_or_name):
        if not user_id_or_name:
            self.logger.debug(
                "Invalid argument to find user ID: " + user_id_or_name
            )
            return None

        self.logger.debug(
            "Trying to find user ID for value: " + user_id_or_name
        )

        # Retrive viewers data.
        viewer_list = self.Parent.GetViewerList()  # list.
        viewer_names = self.Parent.GetDisplayNames(viewer_list)  # dict.

        # Try to find target user by original parameter.
        supposed_name = viewer_names.get(user_id_or_name)
        if supposed_name is not None:
            result = (user_id_or_name, supposed_name)
            self.logger.debug("Found user data (#1): " + str(result))
            return result

        # Try to find target user by original transformed parameter.
        user_id_or_name_low = user_id_or_name.lower()
        supposed_name = viewer_names.get(user_id_or_name_low)
        if supposed_name is not None:
            result = (user_id_or_name_low, supposed_name)
            self.logger.debug("Found user data (#2): " + str(result))
            return result

        self.logger.debug(
            "Quick search failed, need to find among all {0} user names."
            .format(len(viewer_names))
        )

        # Finally, try to find target user among all users manually.
        for user_id, user_name in viewer_names.iteritems():
            if user_id_or_name == user_name:
                result = (user_id, user_name)
                self.logger.debug("Found user data (#3): " + str(result))
                return result
            if user_id_or_name_low == user_name:
                result = (user_id, user_name)
                self.logger.debug("Found user data (#4): " + str(result))
                return result

        self.logger.debug("Cannot find user ID for value: " + user_id_or_name)
        return None

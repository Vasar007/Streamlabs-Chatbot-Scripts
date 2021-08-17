# -*- coding: utf-8 -*-

import transfer_config as config


class TransferPermissionHandler(object):

    def __init__(self, permission, info):
        self.permission = permission
        self.info = info

    def has_permission(self):
        return bool(self.permission)

    def has_info(self):
        return bool(self.info)

    def __str__(self):
        return "{0}: {1}".format(self.permission, self.info)


class TransferPermissionCheckResult(object):
    UserHasHigherPermission = -1
    SamePermissions = 0
    TargetHasHigherPermission = 1


class TransferPermissionChecker(object):

    def __init__(self, parent_wrapper, logger):
        self._parent_wrapper = parent_wrapper
        self._logger = logger

    def check_permissions(self, user_id, target_id, permission_handler):
        """
        Compares user and target permissions and returns result.

        Contract: check of caller user permission should be applied before this
        method call.
        """
        self._logger.debug(
            "Comparing {0} permission with target {1}. Handler: {2}"
            .format(user_id, target_id, permission_handler)
        )

        # Retrieve permissions and compare user and target permissions step by
        # step because we do not have any method to get exactly permission of
        # the selected user.

        start_index = config.PermissionHierarchy.index(
            permission_handler.permission
        )
        for permission in config.PermissionHierarchy[start_index:]:
            check_result = self._compare(
                permission, user_id, target_id, permission_handler
            )
            if check_result is not None:
                return check_result

        # Typically, we should always return earlier.
        # This statement can be reached only if there are more than 1 person
        # which have highest permissions (editor for SL Chatbot).
        return TransferPermissionCheckResult.SamePermissions

    def _compare(self, permission, user_id, target_id, permission_handler):
        should_skip_check = (
            permission == config.UserSpecific and
            not permission_handler.has_info()
        )
        if should_skip_check:
            self._logger.debug(
                "Encountered user_specific permission with no info." +
                "Going to the next permission value to check."
            )
            return None

        has_user_permission = self._parent_wrapper.has_permission(
            user_id, permission, permission_handler.info
        )
        has_target_permission = self._parent_wrapper.has_permission(
            target_id, permission, permission_handler.info
        )
        if has_user_permission and has_target_permission:
            # Should check further.
            return None
        elif has_user_permission and not has_target_permission:
            # User has higher permission.
            return TransferPermissionCheckResult.UserHasHigherPermission
        elif not has_user_permission and has_target_permission:
            # Target has higher permission.
            return TransferPermissionCheckResult.TargetHasHigherPermission
        elif not has_user_permission and not has_target_permission:
            # Both have the same permissions.
            return TransferPermissionCheckResult.SamePermissions

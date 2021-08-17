# -*- coding: utf-8 -*-

class TransferTransaction(object):

    def __init__(self, logger, add_func, remove_func):
        self._logger = logger
        self._add_func = add_func
        self._remove_func = remove_func

        self._add_status = False
        self._add_parameters = None
        self._remove_status = False
        self._remove_parameters = None

        self._committed = False

    def __enter__(self):
        """
        Opens transaction. Initialize class and return actual object to
        process.
        """
        self._logger.debug("Transaction was created.")
        return self

    def __exit__(self, type, value, traceback):
        """
        Closes transaction. If exception occurred, (type, value, traceback)
        will have some values. Otherwise, they will equal to None.

        If __exit__ return True, exception will be swallowed. In case of False,
        exception will propagate.
        """
        if traceback is None:
            # Exit with-block without exception.
            self._logger.debug("Transaction was successfully finished.")
            self._rollback_if_needed_safe()
            return False
        else:
            # Exit with-block with exception.
            self._logger.debug("Transaction was finished with errors.")
            self._rollback_if_needed_safe()
            return False

    def execute_add(self, parameters, send_message):
        """
        Executes add function that passed to transaction.

        If function will execute without any errors, transaction set add
        function flag to success.
        """
        self._add_parameters = parameters
        self._add_status = self._add_func(parameters, send_message)
        if not self._add_status:
            raise RuntimeError("Add points function was failed.")

    def execute_remove(self, parameters, send_message):
        """
        Executes remove function that passed to transaction.

        If function will execute without any errors, transaction set remove
        function flag to success.
        """
        self._remove_parameters = parameters
        self._remove_status = self._remove_func(parameters, send_message)
        if not self._remove_status:
            raise RuntimeError("Remove points function was failed.")

    def commit(self):
        """
        Commits changes. After this function call, rollback will not be called
        implicitly, you should call rollback function by yourself if needed.
        """
        self._committed = True

    def rollback_safe(self):
        """
        Executes rollback for transaction. All executed specified functions
        during transaction will be reverted.
        """
        if not self._add_status and not self._remove_status:
            return

        self._logger.info("Rolling back transaction.")

        if self._add_status:
            self._rollback_add_safe()

        if self._remove_status:
            self._rollback_remove_safe()

    def _rollback_if_needed_safe(self):
        if self._committed:
            self._logger.debug(
                "Rollback is not needed, transaction has been committed."
            )
            return

        self.rollback_safe()

    def _rollback_add_safe(self):
        try:
            self._logger.info("Rolling back add function.")
            self._remove_func(self._add_parameters, send_message=False)
            self._logger.info("Rollback add was finished.")
        except Exception as ex:
            self._logger.exception(
                "Failed to rollback add function: " + str(ex)
            )

    def _rollback_remove_safe(self):
        try:
            self._logger.info("Rolling back remove function.")
            self._add_func(self._remove_parameters, send_message=False)
            self._logger.info("Rollback remove was finished.")
        except Exception as ex:
            self._logger.exception(
                "Failed to rollback remove function: " + str(ex)
            )

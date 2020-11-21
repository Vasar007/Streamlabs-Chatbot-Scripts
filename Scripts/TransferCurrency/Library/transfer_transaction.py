# -*- coding: utf-8 -*-

class TransferTransaction(object):

    def __init__(self, logger, add_func, remove_func):
        self.logger = logger
        self.add_func = add_func
        self.remove_func = remove_func

        self.add_status = False
        self.add_parameters = None
        self.remove_status = False
        self.remove_parameters = None

        self.committed = False

    def __enter__(self):
        """
        Opens transaction. Initialize class and return actual object to
        process.
        """
        self.logger.debug("Transaction was created.")
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
            self.logger.debug("Transaction was successfully finished.")
            self._rollback_if_needed_safe()
            return False
        else:
            # Exit with-block with exception.
            self.logger.debug("Transaction was finished with errors.")
            self._rollback_if_needed_safe()
            return False

    def execute_add(self, parameters, send_message):
        """
        Executes add function that passed to transaction.

        If function will execute without any errors, transaction set add
        function flag to success.
        """
        self.add_parameters = parameters
        self.add_status = self.add_func(parameters, send_message)
        if not self.add_status:
            raise RuntimeError("Add points function was failed.")

    def execute_remove(self, parameters, send_message):
        """
        Executes remove function that passed to transaction.

        If function will execute without any errors, transaction set remove
        function flag to success.
        """
        self.remove_parameters = parameters
        self.remove_status = self.remove_func(parameters, send_message)
        if not self.remove_status:
            raise RuntimeError("Remove points function was failed.")

    def commit(self):
        """
        Commits changes. After this function call, rollback will not be called
        implicitly, you should call rollback function by yourself if needed.
        """
        self.committed = True

    def rollback_safe(self):
        """
        Executes rollback for transaction. All executed specified functions
        during transaction will be reverted.
        """
        if not self.add_status and not self.remove_status:
            return

        self.logger.info("Rolling back transaction.")

        if self.add_status:
            self._rollback_add_safe()

        if self.remove_status:
            self._rollback_remove_safe()

    def _rollback_if_needed_safe(self):
        if self.committed:
            self.logger.debug(
                "Rollback is not needed, transaction has been committed."
            )
            return

        self.rollback_safe()

    def _rollback_add_safe(self):
        try:
            self.logger.info("Rolling back add function.")
            self.remove_func(self.add_parameters, send_message=False)
            self.logger.info("Rollback add was finished.")
        except Exception as ex:
            self.logger.exception(
                "Failed to rollback add function: " + str(ex)
            )

    def _rollback_remove_safe(self):
        try:
            self.logger.info("Rolling back remove function.")
            self.add_func(self.remove_parameters, send_message=False)
            self.logger.info("Rollback remove was finished.")
        except Exception as ex:
            self.logger.exception(
                "Failed to rollback remove function: " + str(ex)
            )

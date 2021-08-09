# -*- coding: utf-8 -*-

import selenium.webdriver as webdriver

import song_request_helpers as helpers
import song_request_config as config

from song_request import SongRequestState
from song_request import SongRequestResult


class SongRequestProcessor(object):

    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger

        self.driver = self._create_browser_driver()

    def __enter__(self):
        """
        Do nothing because all initialization happens in constructor.
        """
        self.logger.debug("Processor was created.")
        return self

    def __exit__(self, type, value, traceback):
        """
        Closes processor. If exception occurred, (type, value, traceback)
        will have some values. Otherwise, they will equal to None.

        If __exit__ return True, exception will be swallowed. In case of False,
        exception will propagate.
        """
        if traceback is None:
            # Exit with-block without exception.
            self.logger.debug("Processor was successfully finished.")
            self.release_resources()
            return False
        else:
            # Exit with-block with exception.
            self.logger.debug("Processor was finished with errors.")
            self.release_resources()
            return False

    def _create_browser_driver(self):
        executable_path = self.settings.BrowserDriverPath

        # Edge
        if self.settings.SelectedBrowserDriver == config.EdgeDriver:
            return webdriver.Edge(executable_path=executable_path)

        # Chrome
        elif self.settings.SelectedBrowserDriver == config.ChromeDriver:
            return webdriver.Chrome(executable_path=executable_path)

        # Firefox.
        elif self.settings.SelectedBrowserDriver == config.FirefoxDriver:
            return webdriver.Firefox(executable_path=executable_path)

        # Opera.
        elif self.settings.SelectedBrowserDriver == config.OperaDriver:
            return webdriver.Opera(executable_path=executable_path)

        # Default case.
        else:
            raise ValueError(
                "Unexpected browser driver type to create: {0}."
                .format(self.settings.SelectedBrowserDriver)
            )

    @helpers.lazy_property
    def _new_song_text_field(self):
        return self.driver.find_element_by_id(
            self.settings.ElementIdOfNewSongTextField
        )

    @helpers.lazy_property
    def _add_song_button(self):
        return self.driver.find_element_by_id(
            self.settings.ElementIdOfAddSongButton
        )

    def release_resources(self):
        self.driver.quit()

    def process(self, song_request):
        self.logger.info(
            "Processing song request [{0}].".format(song_request)
        )

        if song_request.state != SongRequestState.ApprovedAndPending:
            error_message = (
                "Invalid song request to process. Expected " +
                "state {0}, actual state {1}."
                .format(
                    SongRequestState.ApprovedAndPending, song_request.state
                )
            )
            raise ValueError(error_message) 

        
        self._add_new_song(song_request)
        return self._process_result(song_request)

    def _add_new_song(self, song_request):
        self._new_song_text_field.clear()
        self._new_song_text_field.send_keys(song_request.song_link)
        self._add_song_button.click()

    def _process_result(self, song_request):
        notification = self.driver.find_element_by_class_name(
            self.settings.ClassNameOfNotificationIcon
        )

        success = notification.find_element_by_class_name(
            self.settings.ClassNameOfSuccessNotificationIcon
        )
        failure = notification.find_element_by_class_name(
            self.settings.ClassNameOfErrorNotificationIcon
        )
        description = notification.find_element_by_class_name(
            self.settings.ClassNameOfNotificationDescription
        )
        description_text = description.text()

        # Success.
        if success is not None and failure is None:
            self.logger.info(
                "Song request {0} processed successfully. Result: {1}"
                .format(song_request.id, description_text)
            )
            return SongRequestResult.successful(song_request)

        # Failure.
        self.logger.info(
            "Song request {0} processed with failure. Error: {1}"
            .format(song_request.id, description_text)
        )
        return SongRequestResult.failed(song_request, description_text)

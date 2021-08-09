# -*- coding: utf-8 -*-

import threading

import song_request_helpers as helpers

from song_request import SongRequestState


class SongRequestStorage(object):

    def __init__(self, logger):
        self.logger = logger

        self.clear()

    def get_requests_with_single_state(self, state):
        self.logger.info(
            "Getting requests by state {0}.".format(state)
        )

        requests_to_return = self.storage_by_state.get(state)
        return list(requests_to_return)

    def get_requests_with_states(self, *states):
        self.logger.info(
            "Getting requests by {0} states.".format(len(states))
        )

        requests_to_return = list()
        for state in states:
            requests = self.get_requests_with_single_state(state)
            requests_to_return.extend(requests)

        return requests_to_return

    def update_states(self, processed_requests):
        self.logger.info(
            "Updating {0} requests.".format(len(processed_requests))
        )

        for processed_request in processed_requests:
            self.logger.info(
                "Updating request [{0}].".format(processed_request)
            )

            # Update requests in storage by state.
            found_request = self._first_or_default_by_id(
                self.storage_by_state.values(), processed_request
            )
            if found_request is not None:
                prev_list = self.storage_by_state[found_request.state]
                prev_list.remove(found_request)

            list_by_state = self.storage_by_state[processed_request.state]
            list_by_state.append(processed_request)

            # Update requests in storage by state.
            self._update_by_user_id(processed_requests)

    def add_request(self, new_song_request):
        self.logger.info(
            "Adding new request [{0}].".format(new_song_request)
        )

        # Update user's requests.
        self._update_by_user_id(new_song_request)

        # We create lists for all states. No check required.
        list_by_state = self.storage_by_state[new_song_request.state]
        list_by_state.append(new_song_request)

    def clear(self):
        self.storage_by_user_id = dict()

        self.storage_by_state = dict()
        self.storage_by_state[SongRequestState.WaitingForApproval] = list()
        self.storage_by_state[SongRequestState.ApprovedAndPending] = list()
        self.storage_by_state[SongRequestState.ApprovedAndAddedSuccessfully] = list()
        self.storage_by_state[SongRequestState.ApprovedButAddedFailure] = list()
        self.storage_by_state[SongRequestState.Rejected] = list()
        self.storage_by_state[SongRequestState.Cancelled] = list()

    def _update_by_user_id(self, song_request):
        list_by_id = self.storage_by_user_id.get(song_request.user_id)

        if list_by_id is None:
            self.logger.info(
                "No requests found for user ID {0}."
                .format(song_request.user_id)
            )
            list_by_id = list()
            list_by_id.append(song_request)
            self.storage_by_user_id[song_request.user_id] = list_by_id
        else:
            self.logger.info(
                "Some requests found for user ID {0}."
                .format(song_request.user_id)
            )
            found_request = self._first_or_default_by_id(
                list_by_id, song_request
            )
            if found_request is not None:
                list_by_id.remove(found_request)

            list_by_id.append(song_request)
            self.storage_by_user_id[song_request.user_id] = list_by_id

    def _first_or_default_by_id(self, collection, song_request):
        return helpers.first_or_default(
            collection,
            default=None,
            pred=lambda x: x.id == song_request.id
        )

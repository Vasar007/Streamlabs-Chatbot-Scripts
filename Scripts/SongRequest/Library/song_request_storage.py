# -*- coding: utf-8 -*-

import itertools

import song_request_helpers as helpers

from Scripts.SongRequest.CSharp.Models.Requests import SongRequestStateHelper


class SongRequestStorage(object):

    def __init__(self, logger):
        self.logger = logger

        self.storage_by_user_id = dict()
        self.storage_by_state = dict()

        self.clear()

    def get_user_requests(self, user_id):
        self.logger.debug(
            "Getting requests by user ID {0}.".format(user_id)
        )

        requests_to_return = self.storage_by_user_id.get(user_id, list())
        return list(requests_to_return)

    def get_requests_with_single_state(self, state):
        self.logger.debug(
            "Getting requests by state {0}.".format(state)
        )

        requests_to_return = self.storage_by_state.get(state)
        return list(requests_to_return)

    def get_requests_with_states(self, *states):
        self.logger.debug(
            "Getting requests by {0} states.".format(len(states))
        )

        requests_to_return = list()
        for state in states:
            requests = self.get_requests_with_single_state(state)
            requests_to_return.extend(requests)

        return requests_to_return

    def update_states(self, processed_requests):
        self.logger.debug(
            "Updating {0} requests.".format(len(processed_requests))
        )

        for request in processed_requests:
            self.logger.debug(
                "Updating request [{0}].".format(request)
            )

            # Update requests in storage by state.
            all_requests = itertools.chain.from_iterable(
                self.storage_by_state.values()
            )

            found_request = self._first_or_default_by_id(
                all_requests, request
            )
            if found_request:
                prev_list = self.storage_by_state[found_request.State]
                prev_list.remove(found_request)

            list_by_state = self.storage_by_state[request.State]
            list_by_state.append(request)

            # Update requests in storage by state.
            self._update_by_user_id(request)

    def add_request(self, new_song_request):
        self.logger.debug(
            "Adding new request [{0}].".format(new_song_request)
        )

        # Update user's requests.
        self._update_by_user_id(new_song_request)

        # We create lists for all states. No check required.
        list_by_state = self.storage_by_state[new_song_request.State]
        list_by_state.append(new_song_request)

    def remove_request(self, song_request):
        self.logger.debug(
            "Removing request [{0}].".format(song_request)
        )

        # Remove user's request.
        list_by_id = self.storage_by_user_id.get(song_request.UserData.Id)
        if list_by_id and song_request in list_by_id:
            self.logger.debug(
                "Removing request by user ID {0}."
                .format(song_request.UserData.Id)
            )
            list_by_id.remove(song_request)

        # We create lists for all states. No check required.
        list_by_state = self.storage_by_state[song_request.State]
        if song_request in list_by_state:
            self.logger.debug(
                "Removing request by request state {0}."
                .format(song_request.State)
            )
            list_by_state.remove(song_request)

    def clear(self):
        self.storage_by_user_id.clear()

        self.storage_by_state.clear()
        all_states = SongRequestStateHelper.GetAllValues()
        for state in all_states:
            self.logger.debug("Creating list for state '{0}'.".format(state))
            self.storage_by_state[state] = list()

    def _update_by_user_id(self, song_request):
        list_by_id = self.storage_by_user_id.get(song_request.UserData.Id)

        if not list_by_id:
            self.logger.debug(
                "No requests found for user ID {0}. Adding new one."
                .format(song_request.UserData.Id)
            )
            list_by_id = list()
            list_by_id.append(song_request)
            self.storage_by_user_id[song_request.UserData.Id] = list_by_id
        else:
            self.logger.debug(
                "Some requests found for user ID {0}. Updating existing one."
                .format(song_request.UserData.Id)
            )
            found_request = self._first_or_default_by_id(
                list_by_id, song_request
            )
            if found_request:
                list_by_id.remove(found_request)

            list_by_id.append(song_request)
            self.storage_by_user_id[song_request.UserData.Id] = list_by_id

    def _first_or_default_by_id(self, collection, song_request):
        return helpers.first_or_default(
            collection,
            default=None,
            pred=lambda x: x.RequestId == song_request.RequestId
        )

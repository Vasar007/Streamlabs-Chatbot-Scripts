# -*- coding: utf-8 -*-

import score_helpers as helpers


default_player_name = "Player"
default_space_number = 1
default_full_format = "{0} ({1})"


class PlayerScore(object):

    def __init__(self, name, initial_value=0):
        self._name = str(name) if name else default_player_name
        self._value = initial_value if initial_value >= 0 else 0

    def reset(self, initial_value=0):
        self.update(initial_value)

    def increment(self, value=1):
        self.update(self._value + value)

    def decrement(self, value=1):
        self.update(self._value - value)

    def update(self, value):
        if value < 0:
            raise ValueError("Invalid score value: " + str(value))

        self._value = value

    def to_forward_string(self, space_number=1, include_value=True):
        spaces = " " * space_number
        if include_value:
            return self._name + spaces + str(self._value)

        return self._name + spaces

    def to_reversed_string(self, space_number=1, include_value=True):
        spaces = " " * space_number
        if include_value:
            return str(self._value) + spaces + self._name

        return spaces + self._name

    def __str__(self):
        return self.to_forward_string()


class Score(object):

    def __init__(self, logger, player1, player2, description, space_number=1,
                 full_format=None):
        self._logger = logger
        self._player1 = player1
        self._player2 = player2
        self._description = str(description)

        space_number = helpers.safe_cast(space_number, int, 1)
        self._space_number = (
            space_number if space_number >= 1
            else default_space_number
        )

        self._full_format = (
            str(full_format) if full_format
            else default_full_format
        )

    def reset(self):
        self._player1.reset()
        self._player2.reset()
        self._logger.debug("Reseted score for both players.")

    def update(self, player1_score, player2_score, description):
        self._update_player_score(self._player1, player1_score)
        self._update_player_score(self._player2, player2_score)
        self._update_description(description)

    def _update_player_score(self, player, new_score):
        player.update(new_score)
        message = (
            "Updated score for player {0}, new score: {1}"
            .format(player, new_score)
        )
        self._logger.debug(message)

    def _update_description(self, description):
        self._description = str(description)
        message = "Updated score description: {0}".format(description)
        self._logger.debug(message)

    def to_display_string(self, space_number=1, separator_text="vs."):
        player1_string = self._player1.to_forward_string(
            self._space_number, space_number, include_value=False
        )
        player2_string = self._player2.to_reversed_string(
            self._space_number, space_number, include_value=False
        )
        return player1_string + separator_text + player2_string

    def __str__(self):
        score_str = (
            self._player1.to_forward_string(self._space_number) +
            ":" +
            self._player2.to_reversed_string(self._space_number)
        )

        if self._description:
            return self._full_format.format(score_str, self._description)

        return score_str


def fix_player_name_if_needed(player_name, number):
    if player_name:
        return str(player_name)

    return default_player_name + str(number)


def create_score_from_scratch(player1_name, player2_name, description):
    player1_name = fix_player_name_if_needed(player1_name, 1)
    player2_name = fix_player_name_if_needed(player2_name, 2)

    player1 = PlayerScore(player1_name)
    player2 = PlayerScore(player2_name)
    logger = helpers.get_logger()
    score = Score(logger, player1, player2, description)

    message = "Created new score for players: " + str(score)
    logger.debug(message)

    return score

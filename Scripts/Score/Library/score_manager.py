# -*- coding: utf-8 -*-

import score
import score_helpers as helpers
import score_config as config


class ScoreValueHandler(object):

    def __init__(self, is_valid, current_score, message):
        self.is_valid = is_valid
        self.current_score = current_score
        self.message = message


class ScoreManager(object):

    def __init__(self, settings):
        self._settings = settings

        self._active_score = None

    def get_score(self):
        if self._active_score is None:
            message = self._settings.NoScoreFoundMessage
        else:
            message = (
                self._settings.CurrentScoreMessage
                .format(self._active_score)
            )

        return ScoreValueHandler(True, self._active_score, message)

    def create_score(self, player1_name, player2_name, description):
        new_score = score.create_score_from_scratch(
            player1_name, player2_name, description
        )

        if self._active_score is None:
            self._active_score = new_score

            message = self._settings.CreatedScoreMessage.format(new_score)
        else:
            self._active_score = new_score

            message = (
                self._settings.RecreatedScoreMessage
                .format(new_score)
            )

        return ScoreValueHandler(True, self._active_score, message)

    def update_score(self, raw_player1_score, raw_player2_score, description):
        if self._active_score is None:
            message = self._settings.NothingToUpdateMessage
        else:
            (player1_score, message) = self._try_get_score(raw_player1_score)
            if player1_score is None:
                return ScoreValueHandler(False, self._active_score, message)

            (player2_score, message) = self._try_get_score(raw_player2_score)
            if player2_score is None:
                return ScoreValueHandler(False, self._active_score, message)

            self._active_score.update(player1_score, player2_score, description)

            message = (
                self._settings.UpdatedScoreMessage
                .format(self._active_score)
            )

        return ScoreValueHandler(True, self._active_score, message)

    def reset_score(self):
        if self._active_score is None:
            message = self._settings.NothingToResetMessage
        else:
            self._active_score.reset()

            message = self._settings.ResetScoreMessage.format(self._active_score)

        return ScoreValueHandler(True, self._active_score, message)

    def delete_score(self):
        deleted_score = None
        if self._active_score is None:
            message = self._settings.NothingToDeleteMessage
        else:
            deleted_score = self._active_score
            self._active_score = None

            message = (
                self._settings.DeletedScoreMessage
                .format(deleted_score)
            )

        return ScoreValueHandler(True, deleted_score, message)

    def _try_get_score(self, raw_player_score):
        player_score = helpers.safe_cast(raw_player_score, int)
        is_player_score_invalid = (
            player_score is None or
            not self._is_valid_score_value(player_score)
        )
        if is_player_score_invalid:
            message = (
                self._settings.InvalidScoreValueMessage
                .format(raw_player_score, config.ExampleScoreValue)
            )
            return (None, message)

        return (player_score, None)

    def _is_valid_score_value(self, score_value):
        return score_value >= 0

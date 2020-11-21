# -*- coding: utf-8 -*-

import score
import score_helpers as helpers
import score_config as config  # pylint:disable=import-error


class ScoreValueHandler(object):

    def __init__(self, is_valid, current_score, message):
        self.is_valid = is_valid
        self.current_score = current_score
        self.message = message


class ScoreManager(object):

    def __init__(self, settings):
        self.settings = settings

        self.active_score = None

    def get_score(self):
        if self.active_score is None:
            message = self.settings.NoScoreFoundMessage
        else:
            message = (
                self.settings.CurrentScoreMessage
                .format(self.active_score)
            )

        return ScoreValueHandler(True, self.active_score, message)

    def create_score(self, player1_name, player2_name, description):
        new_score = score.create_score_from_scratch(
            player1_name, player2_name, description
        )

        if self.active_score is None:
            self.active_score = new_score

            message = self.settings.CreatedScoreMessage.format(new_score)
        else:
            self.active_score = new_score

            message = (
                self.settings.RecreatedScoreMessage
                .format(new_score)
            )

        return ScoreValueHandler(True, self.active_score, message)

    def update_score(self, raw_player1_score, raw_player2_score, description):
        if self.active_score is None:
            message = self.settings.NothingToUpdateMessage
        else:
            (player1_score, message) = self._try_get_score(raw_player1_score)
            if player1_score is None:
                return ScoreValueHandler(False, self.active_score, message)

            (player2_score, message) = self._try_get_score(raw_player2_score)
            if player2_score is None:
                return ScoreValueHandler(False, self.active_score, message)

            self.active_score.update(player1_score, player2_score, description)

            message = (
                self.settings.UpdatedScoreMessage
                .format(self.active_score)
            )

        return ScoreValueHandler(True, self.active_score, message)

    def reset_score(self):
        if self.active_score is None:
            message = self.settings.NothingToResetMessage
        else:
            self.active_score.reset()

            message = self.settings.ResetScoreMessage.format(self.active_score)

        return ScoreValueHandler(True, self.active_score, message)

    def delete_score(self):
        deleted_score = None
        if self.active_score is None:
            message = self.settings.NothingToDeleteMessage
        else:
            deleted_score = self.active_score
            self.active_score = None

            message = (
                self.settings.DeletedScoreMessage
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
                self.settings.InvalidScoreValueMessage
                .format(raw_player_score, config.ExampleScoreValue)
            )
            return (None, message)

        return (player_score, None)

    def _is_valid_score_value(self, score_value):
        return score_value >= 0

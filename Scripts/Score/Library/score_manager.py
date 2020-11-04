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

    def create_score(self, player1_name, player2_name):
        new_score = score.create_score_from_string(player1_name, player2_name)

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

    def update_score(self, raw_player_id, raw_new_score):
        if self.active_score is None:
            message = self.settings.NothingToUpdateMessage
        else:
            player_id = helpers.safe_cast(raw_player_id, int)
            if player_id is None or not self._is_valid_player_id(player_id):
                message = (
                    self.settings.InvalidPlayerIdMessage
                    .format(raw_player_id, config.ExamplePlayerId)
                )
                return ScoreValueHandler(False, self.active_score, message)

            new_score = helpers.safe_cast(raw_new_score, int)
            if new_score is None or not self._is_valid_score_value(new_score):
                message = (
                    self.settings.InvalidScoreValueMessage
                    .format(raw_new_score, config.ExampleScoreValue)
                )
                return ScoreValueHandler(False, self.active_score, message)

            self.active_score.update_by_string(player_id, new_score)

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

    def _is_valid_player_id(self, player_id):
        return 1 <= player_id <= 2

    def _is_valid_score_value(self, score_value):
        return score_value > 0

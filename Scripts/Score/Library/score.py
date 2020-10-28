# -*- coding: utf-8 -*-

import helpers


class PlayerScore(object):

    def __init__(self, name, initial_score=0):
        self.name = str(name) if not None else "Player"
        self.score = initial_score if initial_score >= 0 else 0

    def reset(self, initial_value=0):
        self.update(initial_value)

    def increment(self, value=1):
        self.update(self.score + value)

    def decrement(self, value=1):
        self.update(self.score - value)

    def update(self, value):
        if value < 0:
            raise ValueError("Invalid score value: " + str(value))

        self.score = value

    def to_forward_string(self, space_number=1):
        spaces = " " * space_number
        return self.name + spaces + str(self.score)

    def to_reversed_string(self, space_number=1):
        spaces = " " * space_number
        return str(self.score) + spaces + self.name

    def __str__(self):
        return self.to_forward_string()


class Score(object):

    def __init__(self, Parent, player1, player2, space_number=1):
        self.Parent = Parent
        self.player1 = player1
        self.player2 = player2
        self.space_number = space_number

    def reset(self):
        self.player1.reset()
        self.player2.reset()
        helpers.log(self.Parent, "Resetted score for both players.")

    def update_by_string(self, player_id, new_score):
        if player_id == 1:
            self._update_player_score(self.player1, new_score)
        elif player_id == 2:
            self._update_player_score(self.player2, new_score)
        else:
            message = (
                "Failed to update score: invalid player ID " + str(player_id)
            )
            helpers.log(self.Parent, message)

    def _update_player_score(self, player, new_score):
        player.update(new_score)
        message = (
            "Updated score for player " + player.name +
            ", new score " + str(new_score)
        )
        helpers.log(self.Parent, message)

    def __str__(self):
        return (
            self.player1.to_forward_string(self.space_number) +
            ":" +
            self.player2.to_reversed_string(self.space_number)
        )


def create_score_from_string(Parent, player1_name, player2_name,
                             space_number=1):
    player1 = PlayerScore(player1_name)
    player2 = PlayerScore(player2_name)
    score = Score(Parent, player1, player2, space_number)

    message = "Created new score: " + str(score)
    helpers.log(Parent, message)

    return score

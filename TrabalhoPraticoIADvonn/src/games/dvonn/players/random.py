from random import randint

from games.dvonn.action import DvonnAction
from games.dvonn.player import DvonnPlayer
from games.dvonn.state import DvonnState
from games.state import State


class RandomDvonnPlayer(DvonnPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: DvonnState):
        return DvonnAction(randint(0,21),randint(0,5))

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass

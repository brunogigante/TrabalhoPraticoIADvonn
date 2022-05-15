from games.dvonn.player import DvonnPlayer
from games.dvonn.state import DvonnState
from games.game_simulator import GameSimulator


class DvonnSimulator(GameSimulator):

    def __init__(self, player1: DvonnPlayer, player2: DvonnPlayer):
        super(DvonnSimulator, self).__init__([player1, player2])

    def init_game(self):
        return DvonnState()

    def before_end_game(self, state: DvonnState):
        # ignored for this simulator
        pass

    def end_game(self, state: DvonnState):
        # ignored for this simulator
        pass

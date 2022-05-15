from games.dvonn.action import DvonnAction
from games.dvonn.player import DvonnPlayer
from games.dvonn.state import DvonnState

class bcolors:
    black = '\033[30m'
    white = '\033[1;97m'
    RESET = '\033[0m'

class HumanDvonnPlayer(DvonnPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: DvonnState):
        state.display()

        while True:
            # noinspection PyBroadException
            try:
                col = int(input(
                    f"Player {bcolors.black + 'Black' + bcolors.RESET if state.get_acting_player() == 0 else bcolors.white + 'White' + bcolors.RESET}, choose a column: "))
                row = int(input(
                    f"Player {bcolors.black + 'Black' + bcolors.RESET if state.get_acting_player() == 0 else bcolors.white + 'White' + bcolors.RESET}, choose a row: "))
                return DvonnAction(col, row)
            except Exception:
                continue

    def event_action(self, pos: int, action, new_state: DvonnState):
        # ignore
        pass

    def event_end_game(self, final_state: DvonnState):
        # ignore
        pass

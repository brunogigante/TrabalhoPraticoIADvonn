from games.dvonn.simulator import DvonnSimulator
from games.game_simulator import GameSimulator
from games.dvonn.players.human import HumanDvonnPlayer
from games.dvonn.players.random import RandomDvonnPlayer


def run_simulation(desc: str, simulator: GameSimulator, iterations: int):
    print(f"----- {desc} -----")

    for i in range(0, iterations):
        simulator.change_player_positions()
        simulator.run_simulation()

    print("Results for the game:")
    simulator.print_stats()


def main():
    print("Dvonn Game Simulator")

    num_iterations = 1

    dvonn_simulations = [
        # uncomment to play as human
        # {
        #     "name": "Yinsh - Human VS Human",
        #     "player1": HumanDvonnPlayer("Human1"),
        #     "player2": HumanDvonnPlayer("Human2")
        # },
        {
           "name": "Yinsh - Random VS Random",
           "player1": HumanDvonnPlayer("Random 1"),
           "player2": RandomDvonnPlayer("Random 2")
        },
        #{
        #    "name": "Yinsh - Greedy VS Random",
        #    "player1": GreedyDvonnPlayer("Greedy"),
        #    "player2": RandomDvonnPlayer("Random")
        #},
        #{
        #    "name": "Minimax VS Random",
        #    "player1": MinimaxDvonnPlayer("Minimax"),
        #    "player2": RandomDvonnPlayer("Random")
        #},
        #{
        #    "name": "Minimax VS Greedy",
        #    "player1": MinimaxDvonnPlayer("Minimax"),
        #    "player2": GreedyDvonnPlayer("Greedy")
        #}
    ]

    for sim in dvonn_simulations:
        run_simulation(sim["name"], DvonnSimulator(sim["player1"], sim["player2"]), num_iterations)

if __name__ == "__main__":
    main()

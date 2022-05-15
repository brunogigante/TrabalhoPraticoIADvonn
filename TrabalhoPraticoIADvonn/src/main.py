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
    global dvonn_simulations
    print("Dvonn Game Simulator")

    num_iterations = 1
    option = 0

    print("1 - Humano vs Humano")
    print("2 - Humano vs Random")

    while option > 2 or option <1:
        option = int(input(f"Escolha o modo de jogo: "))

        if option == 1:
            dvonn_simulations = [
                {
                    "name": "Human VS Human",
                    "player1": HumanDvonnPlayer("Human1"),
                    "player2": HumanDvonnPlayer("Human2")
                }]
        elif option == 2:
            dvonn_simulations = [{
                   "name": "Human VS Random",
                   "player1": HumanDvonnPlayer("Human"),
                   "player2": RandomDvonnPlayer("Random")
                }]


    for sim in dvonn_simulations:
        run_simulation(sim["name"], DvonnSimulator(sim["player1"], sim["player2"]), num_iterations)

if __name__ == "__main__":
    main()

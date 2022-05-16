from typing import Optional
from random import randint

from games.dvonn.action import DvonnAction
from games.dvonn.result import DvonnResult
from games.state import State


class bcolors:
    red = '\033[31m'
    green = '\033[32m'
    blue = '\033[34m'
    cyan = '\033[36m'
    yellow = '\033[33m'
    black = '\033[30m'
    white = '\033[1;97m'
    grey = '\033[1;37m'
    BOLD = '\033[;1m'
    RESET = '\033[0m'


class DvonnState(State):
    EMPTY_CELL = -1

    def __init__(self):
        super().__init__()

        self.__available_plays = 46

        self.__is_completed = False

        """
        the grid
        """
        self.__grid = [[-1, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, -1],
                       [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
                       [0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
                       [-1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1],
                       [-1, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, 0, -1, -1], ]

        # cada posicao valida vai é um tuple
        # (jogador, numero de peças)
        # self.__is_completed = True
        # count = 0
        # for i in range(0, len(self.__grid)):
        #     for j in range(0, len(self.__grid[i])):
        #         if self.__grid[i][j] == 0:
        #             self.__grid[i][j] = (0, 0)
        #             if count == 1:
        #                 self.__grid[i][j] = (1, 23)
        #             elif count == 2:
        #                 self.__grid[i][j] = (2, 23)
        #             else:
        #                 self.__grid[i][j] = (0, 0)
        #             count += 1
        #         else:
        #             self.__grid[i][j] = (-1, 0)

        self.__first_play()

        # completar automaticamente a grid com 23 peças de cada cor para jogar diretamente na momento das stacks
        # for i in range(0, 22):
        #     __is__valid = False
        #     while not __is__valid:
        #         row = randint(0, 4)
        #         col = randint(0, 20)
        #         player, num_pieces = self.__grid[row][col]
        #         if player == 0:
        #             __is__valid = True
        #             self.__grid[row][col] = (1, 1)
        #             self.__available_plays -= 1
        #             if self.__available_plays == 0:
        #                 self.__is_completed = True
        #
        # for i in range(0, 22):
        #     __is__valid = False
        #     while not __is__valid:
        #         row = randint(0, 4)
        #         col = randint(0, 20)
        #         player, num_pieces = self.__grid[row][col]
        #         if player == 0:
        #             __is__valid = True
        #             self.__grid[row][col] = (2, 1)
        #             self.__available_plays -= 1
        #             if self.__available_plays == 0:
        #                 self.__is_completed = True


        """
        counts the number of turns in the current game
        """
        self.__turns_count = 2

        """
        the index of the current acting player
        """
        self.__acting_player = 1

        """
        determine if a winner was found already 
        """
        self.__has_winner = False

        self.__last_play = (-1, -1)

        self.__is_selecting = True

        self.__draw = False

    def __first_play(self):
        valid_plays = 0
        while valid_plays != 3:
            row = randint(0, 4)
            col = randint(0, 20)

            # player, num_pieces = (1, 3)
            #   1   ,     3
            player, num_pieces = self.__grid[row][col]

            if player != -1:
                self.__grid[row][col] = (3, 1)
                valid_plays += 1

    def __check_winner(self, player):
        stacks_on_field = []
        amount_player = 0
        amount_other_player = 0
        for row in range(0, 5):
            for col in range(0, 21):
                player_num, num_pieces = self.__grid[row][col]
                if player_num > 0:
                    stacks_on_field.append(self.__grid[row][col])
                    if player_num == player:
                        amount_player += 1
                    elif player_num != player:
                        amount_other_player += 1

        if amount_other_player == 0:
            print("O player", bcolors.black + "Black" + bcolors.RESET if player == 1 else bcolors.white + 'White' + bcolors.RESET, "ganhou!")
            return True


        if len(stacks_on_field) == 2:
            values = [val for p, val in stacks_on_field]
            print("Values: ", values)
            if values[0] == values[1]:
                self.__draw = True
                print("Os players empataram!")
                return True
            stacks_on_field.sort(key=lambda x:x[1])
            player_num, num_pieces = stacks_on_field.pop()
            if player_num == player:
                print("O player", bcolors.black + "Black" + bcolors.RESET if player == 1 else bcolors.white + 'White' + bcolors.RESET, "ganhou!")
                return True

    def get_grid(self):
        return self.__grid

    def get_num_players(self):
        return 2

    def validate_action(self, action: DvonnAction) -> bool:
        col = action.get_col()
        row = action.get_row()
        last_row, last_col = self.__last_play
        last_player, last_numPieces = self.__grid[last_row][last_col]

        if col < 0 or col > 20:
            return False

        if row < 0 or row > 4:
            return False

        player, num_pieces = self.__grid[row][col]

        if player == DvonnState.EMPTY_CELL:
            return False

        if not self.__is_completed:
            if player == 3:
                return False
            if player != 0:
                return False
        elif self.__is_completed and self.__is_selecting:
            if player != self.__acting_player and player != 0:
                return False

        if self.__is_completed:
            if player == -2:
                return False

            if 0 <= row <= 4:
                # verificar nao permitir selecionar peça vazia (verificar se o player é 0 quando a tabela esta completa)
                if self.__is_selecting:
                    if player == 0:
                        return False
                else:
                    # verificaçoes movimentaçao na vertical
                    if last_col == col:
                        if last_row < row:
                            if (row / 2) > last_numPieces:
                                return False
                        else:
                            if ((last_row - row) / 2) > last_numPieces:
                                return False

                    # verificaçoes movimentaçao na horizontal
                    if last_row == row:
                        if last_col < col:
                            if (col / 2) > last_numPieces:
                                return False
                        else:
                            if ((last_col - col) / 2) > last_numPieces:
                                return False

                    # verificaçoes movimentaçao na diagonal
                    if last_row != row and last_col != col:
                        row_diff = abs(last_row - row)
                        col_diff = abs(col - last_col)
                        if row_diff != col_diff:
                            return False
                        if row_diff > last_numPieces:
                            return False


                if self.__available_plays != 0:
                    # verificaçoes para jogadas após a primeira
                    pass
                else:
                    if self.__is_selecting:
                        if row == 2 and col not in [0, 20]:
                            return False
                        elif row in [1, 3] and col not in [1, 19]:
                            return False

        return True

    def update(self, action: DvonnAction):
        col = action.get_col()
        row = action.get_row()
        player, num_pieces = self.__grid[row][col]

        if self.__is_completed and self.__is_selecting:
            self.__grid[row][col] = (-2, num_pieces)
        elif self.__is_completed and not self.__is_selecting:
            last_row, last_col = self.__last_play
            _,lastNumPieces = self.__grid[last_row][last_col]
            self.__grid[row][col] = (self.__acting_player, num_pieces + lastNumPieces)
            self.__grid[last_row][last_col] = (0, 0)
            self.__available_plays += 1
        else:
            self.__grid[row][col] = (self.__acting_player, 1)

        if not self.__is_completed:
            self.__available_plays -= 1

        if self.__is_completed:
            # determine if there is a winner
            self.__has_winner = self.__check_winner(self.__acting_player)

        if self.__is_completed and not self.__is_selecting:
            self.__is_selecting = True
            # switch to next player
            self.__acting_player = 1 if self.__acting_player == 2 else 2
            self.__turns_count += 1
        elif self.__is_completed and self.__is_selecting:
            self.__is_selecting = False

        if not self.__is_completed:
            # switch to next player
            self.__acting_player = 1 if self.__acting_player == 2 else 2
            self.__turns_count += 1

        if self.__available_plays == 0:
            self.__is_completed = True

        self.__last_play = (row, col)

    def __display_cell(self, row, col):

        player, num_pieces = self.__grid[row][col]

        if num_pieces > 1:
            if player == -2:
                print(bcolors.yellow + f'{num_pieces}' + bcolors.RESET, end="")
            else:
                print((bcolors.white if player == 2 else bcolors.black) + f'{num_pieces}' + bcolors.RESET, end="")
        else:
            if player == 0:
                print(bcolors.white + '∙' + bcolors.RESET, end="")
            elif player == 1:
                print(bcolors.black + '◯' + bcolors.RESET, end="")
            elif player == 2:
                print(bcolors.white + '◯' + bcolors.RESET, end="")
            elif player == 3:
                print(bcolors.red + '◯' + bcolors.RESET, end="")
            elif player == -2:
                print(bcolors.yellow + '◯' + bcolors.RESET, end="")
            elif player == DvonnState.EMPTY_CELL:
                print(' ', end="")

    def __display_numbers(self):
        print('   ', end="")
        for col in range(0, 21):
            if col < 21:
                print('   ', end="")
            print(col, end="")
        print("")

    def display(self):
        self.__display_numbers()

        for row in range(0, 5):
            if row < 5:
                print(row, '    ', end="")
            else:
                print(row, '   ', end="")
            for col in range(0, 21):
                self.__display_cell(row, col)
                print('   ', end="")
            print("")

        self.__display_numbers()
        print("")

    def __is_full(self):
        return self.__turns_count > (5 * 21)

    def is_finished(self) -> bool:
        return self.__has_winner or self.__is_full()

    def get_acting_player(self) -> int:
        return self.__acting_player - 1

    def clone(self):
        cloned_state = DvonnState()
        cloned_state.__turns_count = self.__turns_count
        cloned_state.__acting_player = self.__acting_player
        cloned_state.__has_winner = self.__has_winner
        for row in range(0, 5):
            for col in range(0, 21):
                cloned_state.__grid[row][col] = self.__grid[row][col]
        return cloned_state

    def get_result(self, pos) -> Optional[DvonnResult]:
        if self.__has_winner and self.__draw:
            return DvonnResult.DRAW
        if self.__has_winner:
            return DvonnResult.LOOSE if pos == self.__acting_player else DvonnResult.WIN
        if self.__is_full():
            return DvonnResult.DRAW
        return None

    def get_num_rows(self):
        return 5

    def get_num_cols(self):
        return 21

    def before_results(self):
        pass

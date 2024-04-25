import os
import time


# placeholder to mark board
PLACEHOLDER = {
    0: "X",  # player's placeholder
    1: "O",  # AI's placeholder
}


# Exception for gamestop
class StopGame(Exception):
    pass


class Board:
    # private board init
    def __init__(self) -> None:
        self.__board = [
            ["-", "-", "-"],
            ["-", "-", "-"],
            ["-", "-", "-"],
        ]

    # board getter
    def get_board(self, row: int, col: int) -> str:
        return self.__board[row][col]

    # board setter
    def set_board(self, row: int, col: int, value: str) -> None:
        self.__board[row][col] = value

    # check winning conditions and return score
    def get_score(self, depth: int = 0) -> tuple[int, int]:
        # winning board states
        win_board = [
            [self.__board[0][0], self.__board[0][1], self.__board[0][2]],
            [self.__board[1][0], self.__board[1][1], self.__board[1][2]],
            [self.__board[2][0], self.__board[2][1], self.__board[2][2]],
            [self.__board[0][0], self.__board[1][0], self.__board[2][0]],
            [self.__board[0][1], self.__board[1][1], self.__board[2][1]],
            [self.__board[0][2], self.__board[1][2], self.__board[2][2]],
            [self.__board[0][0], self.__board[1][1], self.__board[2][2]],
            [self.__board[2][0], self.__board[1][1], self.__board[0][2]],
        ]
        for row in win_board:
            if all(map(lambda x: x == PLACEHOLDER[0], row)):
                return 1, -10  # return WIN and -10 points - human won
            if all(map(lambda x: x == PLACEHOLDER[1], row)):
                return 1, 10  # return WIN and +10 points - AI won
        return 0, 0  # no winner

    # check if there are free spots left on board and return them
    def get_free_spots(self) -> set[tuple[int, int]]:
        return set(
            (
                irow,
                icol,
            )
            for irow, row in enumerate(self.__board)
            for icol, pos in enumerate(row)
            if pos == "-"
        )

    # clear screen
    def clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    # prints error with timer
    def print_error(self, t: int) -> None:
        for t_ in range(t, 0, -1):
            self.print_board(player="Player", error=t_)
            time.sleep(1)

    # prints board
    def print_board(
        self, player: str = None, error: str = None, gameover: bool = False
    ) -> None:
        self.clear_screen()
        # header print
        if player:
            print(f"{player}'s turn...\n")
        if gameover:
            print("Game over!\n")
        # table print
        print("  0 1 2")
        for irow, row in enumerate(self.__board):
            print(irow, " ".join(row))
        print()
        # error print
        if error is not None:
            print(
                f"Input error - wrong value or trying to point ocupied spot, try again - {error}..."
            )


# main function based on minimax algorithm (DFS)
def minimax(board: Board, isAI: bool, depth: int) -> int:

    # define initial best score based on current player
    if isAI:
        bestScore = float("-inf")
    else:
        bestScore = float("inf")

    # check winning conditinons
    currentState = board.get_score(depth=depth)
    if currentState[0]:
        score = currentState[1]
        return score

    # if there are free spots
    if freeSpots := board.get_free_spots():
        for row, col in freeSpots:
            # mark next spot available
            board.set_board(row, col, PLACEHOLDER[isAI])
            # go deeper in recursion
            score = minimax(board, not isAI, depth + 1)
            # restore previous state
            board.set_board(row, col, "-")
            if isAI:  # if maximizing player - AI in our case
                bestScore = max(score - depth, bestScore)
            else:  # if minimizing player - HUMAN in our case
                bestScore = min(score + depth, bestScore)
        return bestScore
    else:
        return 0

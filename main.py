"""
TicTacToe game player vs AI based on minimax algotithm

Known limitations:
1. Player always goes first with 'X', no customization
2. Superficial exception handling
"""

import os
import time

from minimax import minimax, PLACEHOLDER, StopGame, Board


# check if this is player's turn
def is_player_turn(turn: int) -> bool:
    return not (turn % 2)


# entry point into recursion
def entry_point_AI(board: Board) -> tuple[int, int]:
    bestScore = float("-inf")
    if freeSpots := board.get_free_spots():
        for row, col in freeSpots:
            board.set_board(row, col, PLACEHOLDER[1])
            score = minimax(board, False, 0)
            board.set_board(row, col, "-")
            if score > bestScore:
                bestScore = score
                pos = (row, col)
    return pos

if __name__ == "__main__":
    # Player makes his turn (X) first
    board = Board()
    turn = 0
    isStoppedByPlayer= False    
    playerWon = False
    aiWon = False
    draw = False
    
    while not (isStoppedByPlayer or playerWon or aiWon or draw):

        while freeSpots := board.get_free_spots():

            # Player's turn
            if is_player_turn(turn):

                try:
                    board.print_board(player="Player")
                    pos = input(
                        "Enter row and column to place 'X'(for example - 0 3), press Q for exit:  "
                    )
                    # check if player wants to quit
                    if pos.lower() == "q":
                        raise StopGame
                    row, col = tuple(map(int, pos.split()))
                    # if coordinates are not valid raise exception
                    if (row, col) not in freeSpots:
                        raise ValueError
                    # mark spot
                    board.set_board(row, col, PLACEHOLDER[0])
                    # check for winner
                    if board.get_score()[0]:
                        playerWon = True
                        break
                    turn += 1

                except (TypeError, ValueError) as err:
                    board.print_error(3)
                    break

                except StopGame: break

            # AI's turn, minimax algorithm
            else:
                board.print_board(player="AI")
                row, col = entry_point_AI(board)
                board.set_board(row, col, PLACEHOLDER[1])
                # check for winner
                if board.get_score()[0]:
                    aiWon = True
                    break
                turn += 1
        else:
            draw = True

    board.print_board(gameover=True)

    print("Game result: {}".format("Draw..." if draw else
                                "AI won!" if aiWon else
                                "Player won!" if playerWon else
                                "Game was ended by user."))

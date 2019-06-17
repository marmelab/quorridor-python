import math
from pawn import Pawn, translate_x, translate_y
from exception import QuoridorException, OutOfBoardException, UnknownActionException
from functools import reduce
from action import Action
import console
from board import *


def init_game():
    center = math.floor(BASE_LINE_SIZE / 2)
    return [Pawn(0, center), Pawn(BASE_LINE_SIZE -1, center)]


def progress(pawns):
    new_pawns = pawns
    new_fences = build()
    player_turn = 1
    quit = False
    victory = False
    console.clear()
    console.prompt("** Welcome to PyQuoridor **\n  Press Enter to start ...")
    while not(quit or victory):
        display(new_pawns, new_fences)
        action = console.prompt_action(player_turn)
        if action == Action.EXIT:
            quit = True
        else:
            try:
                new_pawn = act(action, new_pawns[player_turn - 1], new_fences)
                new_pawns = deepcopy(new_pawns)
                new_pawns[player_turn - 1] = new_pawn
            except QuoridorException:
                pass
        victory = is_a_victory(new_pawns)
    if victory:
        display(new_pawns, new_fences)
        console.display("** You won **")


def display(pawns, fences):
    console.clear()
    board = get_board(pawns, fences)
    console.display_game(board)


def is_a_victory(pawns):
    #TODO direction
    return pawns[0].x == BASE_LINE_SIZE - 1


def act(action, pawn, fences):
    new_pawn = None
    if action == Action.RIGHT:
        new_pawn = move_right(pawn, fences)
    elif action == Action.LEFT:
        new_pawn = move_left(pawn, fences)
    elif action == Action.DOWN:
        new_pawn = move_down(pawn, fences)
    elif action == Action.UP:
        new_pawn = move_up(pawn, fences)
    else:
        raise UnknownActionException()
    if is_out_of_board(new_pawn):
        raise OutOfBoardException("The pawn is out of the board")
    return new_pawn


def move_right(pawn, fences):
    if not is_crossable_right(pawn, fences):
        raise OutOfBoardException("The pawn cannot cross")
    return translate_x(pawn, 2)


def move_left(pawn, fences):
    if not is_crossable_left(pawn, fences):
        raise OutOfBoardException("The pawn cannot cross")
    return translate_x(pawn, -2)


def move_up(pawn, fences):
    if not is_crossable_up(pawn, fences):
        raise OutOfBoardException("The pawn cannot cross")
    return translate_y(pawn, -2)


def move_down(pawn, fences):
    if not is_crossable_down(pawn, fences):
        raise OutOfBoardException("The pawn cannot cross")
    return translate_y(pawn, 2)

"""
# ----------------------------------------------------------------------------
#     Name: BlankAlgorithm.py
#     Purpose: Algorithm that takes a random choice out of all possible paths.
#
#     IMPORTANT: To move the robot, just change the coordinates.
#
#     Author: CUONG NGUYEN
#
#     Last Modified: 8/4/2020
# ----------------------------------------------------------------------------
"""
from MazeMod import ParentMaze
import random


class Maze(ParentMaze):
    """ Child class of ParentMaze
    Add or modify functions to suit your algorithm """
    pass


def cell(x, y):
    """ For easy access. Generally no need to modify"""
    return Maze.cell(x, y)


def sensor_cell(x, y):
    """ For easy access. Generally no need to modify """
    return Maze.sensor_cell(x, y)


def create():
    """ For easy access. Generally no need to modify """
    Maze.create()


def maze_print():
    """ For debugging. Generally no need to modify """
    Maze.print()


def sensor_print():
    """ For debugging. Generally no need to modify """
    Maze.sensor_print()


def cur_pos():
    """ Return the current position of the mouse """
    return x, y


# record current position
x, y = 0, 0
# prevent going backward without being at a corner
previous_choice = ""


def atCenter():
    """ Determine the robot has reached the center cells """
    global x, y
    if 9 > x > 6 and 9 > y > 6:
        return True
    return False


def reset():
    """ Reset the memory before traversing the maze"""
    global x, y
    Maze.clear_mem()
    x, y = 0, 0
    cell(0, 0).set_checked(True)


def run_algorithm():
    """ The algorithm which is to be iterated until the center is reached
    Return "done" if the center is reached, return "not done" otherwise """
    global x, y, previous_choice
    if atCenter():
        return "done"
    choices = []
    if not sensor_cell(x, y).north_wall:
        choices.append("n")
    if not sensor_cell(x, y).south_wall:
        choices.append("s")
    if not sensor_cell(x, y).west_wall:
        choices.append("w")
    if not sensor_cell(x, y).east_wall:
        choices.append("e")
    # prevent going backward without being at a corner
    # not important in a real mouse (just don't use the reverse function)
    if len(choices) != 1:
        if previous_choice == "n" and "s" in choices:
            choices.remove("s")
        elif previous_choice == "s" and "n" in choices:
            choices.remove("n")
        elif previous_choice == "w" and "e" in choices:
            choices.remove("e")
        elif previous_choice == "e" and "w" in choices:
            choices.remove("w")

    path = random.choice(choices)
    previous_choice = path
    if path == "n":  # advance north
        y += 1
    elif path == "s":  # advance south
        y -= 1
    elif path == "w":  # advance west
        x -= 1
    else:  # advance east
        x += 1
    cell(x, y).set_checked(True)
    return "not done"

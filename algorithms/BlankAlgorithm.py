"""
# ----------------------------------------------------------------------------
#     Name: BlankAlgorithm.py
#     Purpose: Make a copy of this file and modify into your own algorithm.
#              What included in here is REQUIRED for compatibility with the
#              app.
#
#     IMPORTANT: To move the robot, just change the coordinates.
#
#     Author: CUONG NGUYEN
#
#     Last Modified: 8/8/2020
# ----------------------------------------------------------------------------
"""
from MazeMod import ParentMaze


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
    """ Return the current position of the mouse. Generally no need to modify """
    return x, y


x, y = 0, 0  # record current position


def at_center():
    """ Determine if the robot has reached the center cells """
    return True


def reset():
    """ Reset the memory before traversing the maze"""
    global x, y
    Maze.clear_mem()
    x, y = 0, 0


def run_algorithm():
    """ The algorithm which is to be iterated until the center is reached
    Return "done" if the center is reached, return "not done" otherwise """
    if at_center():
        return "done"
    return "not done"

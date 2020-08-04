"""
# ----------------------------------------------------------------------------
#     Name: BlankAlgorithm.py
#     Purpose: Make a copy of this file and modify into your own algorithm.
#              What included in here is REQUIRED for compatibility with the
#              app.
#
#     Author: CUONG NGUYEN
#
#     Last Modified: 8/3/2020
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
    """ Return the current position of the mouse """
    return 0, 0


def reset():
    """ Reset the memory before traversing the maze"""
    Maze.clear_mem()


def run_algorithm():
    """ The algorithm which is to be iterated until the center is reached
    Return "done" if the center is reached, return "not done" otherwise """
    return "done"

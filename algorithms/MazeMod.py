"""
# ----------------------------------------------------------------------------
#     Name: ParentMaze.py
#     Purpose: Class for the maze object and operations on it.
#              Maze represents what robot actually sees.
#              Sensor maze represents the setting of real maze
#
#     Authors: CUONG NGUYEN & Matt-HP
#
#     Last Modified: 8/3/2020
# ----------------------------------------------------------------------------
"""
from CellMod import Cell
import random


class ParentMaze:
    """ Class to store mazes of different perspectives for the robot"""

    sensor_maze = [[Cell() for y in range(16)] for x in range(16)]

    maze = [[Cell() for n in range(16)] for m in range(16)]
    # Maze has edge walls
    for i in range(16):
        maze[i][0].set_south_wall(True)
        maze[0][i].set_west_wall(True)
        maze[i][15].set_north_wall(True)
        maze[15][i].set_east_wall(True)
    maze[0][0].set_east_wall(True)
    maze[1][0].set_west_wall(True)

    unvisited_stack = []

    @classmethod
    def sensor_cell(cls, x: int, y: int):
        """ Return the cell of the actual maze at the given coordinate """
        return cls.sensor_maze[x][y]

    @classmethod
    def cell(cls, x: int, y: int):
        """Return the cell of robot's virtual maze at the given coordinate"""
        return cls.maze[x][y]

    @classmethod
    def print(cls):
        """ Print out robot's virtual maze in its
        current state to the console """
        print("___________________________________________________________\n")
        print("+", end="")
        for j in range(16):
            print("----+", end="")
        print()
        for j in reversed(range(16)):
            print("|", end="")
            for i in range(16):
                print("    ", end="")
                if cls.maze[i][j].east_wall:
                    print("|", end="")
                else:
                    print(" ", end="")
            print()
            print("+", end="")
            for i in range(16):
                if cls.maze[i][j].south_wall:
                    print("----+", end="")
                else:
                    print("    +", end="")
            print()

    @classmethod
    def sensor_print(cls):
        """ Print out the actual maze to the console """
        print("___________________________________________________________\n")
        print("+", end="")
        for j in range(16):
            print("----+", end="")
        print()
        for j in reversed(range(16)):
            print("|", end="")
            for i in range(16):
                print("    ", end="")
                if cls.sensor_maze[i][j].east_wall:
                    print("|", end="")
                else:
                    print(" ", end="")
            print()
            print("+", end="")
            for i in range(16):
                if cls.sensor_maze[i][j].south_wall:
                    print("----+", end="")
                else:
                    print("    +", end="")
            print()

    @classmethod
    def available_neighbor(cls, x: int, y: int):
        """ For use with creating the actual maze
        Return whether there is an available neighbor """
        if y < 15 and not cls.sensor_maze[x][y+1].checked:
            cls.unvisited_stack.append([x, y+1])
            return True
        if y > 0 and not cls.sensor_maze[x][y-1].checked:
            cls.unvisited_stack.append([x, y-1])
            return True
        if x < 15 and not cls.sensor_maze[x+1][y].checked:
            cls.unvisited_stack.append([x+1, y])
            return True
        if x > 0 and not cls.sensor_maze[x-1][y].checked:
            cls.unvisited_stack.append([x-1, y])
            return True
        return False

    @classmethod
    def create(cls):
        """ Create a random organic maze """
        # Fill the sensor_maze with walls to prepare for creation
        for i in range(16):
            for j in range(16):
                cls.sensor_maze[i][j].set_north_wall(True)
                cls.sensor_maze[i][j].set_south_wall(True)
                cls.sensor_maze[i][j].set_west_wall(True)
                cls.sensor_maze[i][j].set_east_wall(True)
                cls.sensor_maze[i][j].set_checked(False)
        cls.unvisited_stack = []

        # Start square is bounded on three sides by walls.
        cls.sensor_maze[0][0].set_checked(True)
        cls.sensor_maze[0][0].set_north_wall(False)
        cls.sensor_maze[0][1].set_south_wall(False)

        i = 0
        j = 1
        k = 1
        visited_stack = []

        while k < 255:  # 16*16 - 1
            path = []
            cls.sensor_maze[i][j].set_checked(True)
            if [i, j] in cls.unvisited_stack:
                cls.unvisited_stack.remove([i, j])
            if cls.available_neighbor(i, j):
                visited_stack.append([i, j])
                if i < 15 and not cls.sensor_maze[i+1][j].checked:
                    path.append("r")
                if i > 0 and not cls.sensor_maze[i-1][j].checked:
                    path.append("l")
                if j < 15 and not cls.sensor_maze[i][j+1].checked:
                    path.append("u")
                if j > 0 and not cls.sensor_maze[i][j-1].checked:
                    path.append("d")

                destination = random.choice(path)
                if destination == "u":
                    cls.sensor_maze[i][j].set_north_wall(False)
                    cls.sensor_maze[i][j+1].set_south_wall(False)
                    j += 1
                elif destination == "d":
                    cls.sensor_maze[i][j].set_south_wall(False)
                    cls.sensor_maze[i][j-1].set_north_wall(False)
                    j -= 1
                elif destination == "r":
                    cls.sensor_maze[i][j].set_east_wall(False)
                    cls.sensor_maze[i+1][j].set_west_wall(False)
                    i += 1
                else:
                    cls.sensor_maze[i][j].set_west_wall(False)
                    cls.sensor_maze[i-1][j].set_east_wall(False)
                    i -= 1
                k += 1

            elif len(visited_stack) != 0:
                i = visited_stack[-1][0]
                j = visited_stack[-1][1]
                visited_stack.pop()

        cls.sensor_maze[7][7].set_north_wall(False)
        cls.sensor_maze[7][7].set_east_wall(False)
        cls.sensor_maze[7][8].set_east_wall(False)
        cls.sensor_maze[7][8].set_south_wall(False)
        cls.sensor_maze[8][7].set_north_wall(False)
        cls.sensor_maze[8][7].set_west_wall(False)
        cls.sensor_maze[8][8].set_south_wall(False)
        cls.sensor_maze[8][8].set_west_wall(False)

    @classmethod
    def clear_mem(cls):
        """ Reset the mouse's memory of the virtual maze """
        for i in range(16):
            for j in range(16):
                cls.maze[i][j].set_north_wall(False)
                cls.maze[i][j].set_south_wall(False)
                cls.maze[i][j].set_west_wall(False)
                cls.maze[i][j].set_east_wall(False)
                cls.maze[i][j].set_checked(False)
                cls.maze[i][j].step = 256
        for i in range(16):
            cls.maze[i][0].set_south_wall(True)
            cls.maze[0][i].set_west_wall(True)
            cls.maze[i][15].set_north_wall(True)
            cls.maze[15][i].set_east_wall(True)
        cls.maze[0][0].set_east_wall(True)
        cls.maze[1][0].set_west_wall(True)

    @classmethod
    def clear_sensor_maze(cls):
        """ Reset the mouse's memory of the virtual maze """
        for i in range(16):
            for j in range(16):
                cls.sensor_maze[i][j].set_north_wall(False)
                cls.sensor_maze[i][j].set_south_wall(False)
                cls.sensor_maze[i][j].set_west_wall(False)
                cls.sensor_maze[i][j].set_east_wall(False)
        for i in range(16):
            cls.sensor_maze[i][0].set_south_wall(True)
            cls.sensor_maze[0][i].set_west_wall(True)
            cls.sensor_maze[i][15].set_north_wall(True)
            cls.sensor_maze[15][i].set_east_wall(True)
        cls.sensor_maze[0][0].set_east_wall(True)
        cls.sensor_maze[1][0].set_west_wall(True)


if __name__ == "__main__":
    ParentMaze.sensor_print()

"""
# ----------------------------------------------------------------------------
#     Name: ModifiedFloodFill.py
#     Purpose: Modified flood algorithm demonstration based on
#              Prof. George Law from California State University, Northridge
#              - Cost less RAM
#              - Run much faster
#
#     IMPORTANT: To move the robot, just change the coordinates.
#
#     Author: CUONG NGUYEN
#
#     Last Modified: 8/4/2020
# ----------------------------------------------------------------------------
"""
from MazeMod import ParentMaze


class Maze(ParentMaze):
    """ Child class of ParentMaze """
    @classmethod
    def print(cls):
        """ Print out robot's virtual maze in its current state to the console
            (This function overrides the print function from Mazemod, not always
            necessary for every algorithm) """
        step_width = len(str(cls.maze[0][0].step))
        print("___________________________________________________________\n")
        print("+", end="")
        for j in range(16):
            print("-" * (step_width + 2) + "+", end="")
        print()
        for j in reversed(range(16)):
            print("|", end="")
            for i in range(16):
                total_space = step_width - len(str(cls.maze[i][j].step)) + 2
                front = int(total_space/2)
                back = total_space - front
                print(" " * front + str(cls.maze[i][j].step)
                      + " " * back, end="")
                if cls.maze[i][j].east_wall:
                    print("|", end="")
                else:
                    print(" ", end="")
            print()
            print("+", end="")
            for i in range(16):
                if cls.maze[i][j].south_wall:
                    print("-" * (step_width + 2) + "+", end="")
                else:
                    print(" " * (step_width + 2) + "+", end="")
            print()


def cell(x, y):
    """ For easy access """
    return Maze.cell(x, y)


def sensor_cell(x, y):
    """ For easy access """
    return Maze.sensor_cell(x, y)


def create():
    """ For easy access """
    Maze.create()


def maze_print():
    """ For debugging """
    Maze.print()


def sensor_print():
    """ For debugging """
    Maze.sensor_print()


def cur_pos():
    """ Return the current position of the mouse """
    global i, j
    return i, j


# record current position
i = 0
j = 0
# initialize variables for current wall info, starts at (0, 0)
curr_north_wall = False
curr_south_wall = True
curr_west_wall = True
curr_east_wall = True
require_flooding = False  # record if current update needs another flood


def read_wall():
    """ Read wall info, either by sensors, or from previous run
    If no new wall is found, no flooding is required """
    global curr_north_wall, curr_south_wall, curr_east_wall, curr_west_wall,\
        require_flooding
    curr_north_wall = sensor_cell(i, j).north_wall
    curr_south_wall = sensor_cell(i, j).south_wall
    curr_west_wall = sensor_cell(i, j).west_wall
    curr_east_wall = sensor_cell(i, j).east_wall
    require_flooding = False

    if cell(i, j).north_wall != curr_north_wall:
        require_flooding = True
        cell(i, j).set_north_wall(curr_north_wall)
        if j < 15:
            cell(i, j+1).set_south_wall(curr_north_wall)

    if cell(i, j).south_wall != curr_south_wall:
        require_flooding = True
        cell(i, j).set_south_wall(curr_south_wall)
        if j > 0:
            cell(i, j-1).set_north_wall(curr_south_wall)

    if cell(i, j).west_wall != curr_west_wall:
        require_flooding = True
        cell(i, j).set_west_wall(curr_west_wall)
        if i > 0:
            cell(i-1, j).set_east_wall(curr_west_wall)

    if cell(i, j).east_wall != curr_east_wall:
        require_flooding = True
        cell(i, j).set_east_wall(curr_east_wall)
        if i < 15:
            cell(i+1, j).set_west_wall(curr_east_wall)


def advance():
    """ Move to the next best path """
    global i, j
    shortest = 1000
    path = ""
    if j < 15 and not curr_north_wall:
        shortest = cell(i, j+1).step
        path = "n"
    if j > 0 and not curr_south_wall and cell(i, j-1).step < shortest:
        shortest = cell(i, j-1).step
        path = "s"
    if i < 15 and not curr_east_wall and cell(i+1, j).step < shortest:
        shortest = cell(i+1, j).step
        path = "e"
    if i > 0 and not curr_west_wall and cell(i-1, j).step < shortest:
        path = "w"

    if path == "n":  # advance north
        j += 1
    elif path == "s":  # advance south
        j -= 1
    elif path == "w":  # advance west
        i -= 1
    else:  # advance east
        i += 1
    cell(i, j).set_checked(True)


def initial_flood():
    """ Initially flood the maze with distances from center """
    for x in range(16):
        for y in range(16):
            if x < 8 and y < 8:
                cell(x, y).set_step(14 - x - y)  # 7 - x + 7 - y
            elif x > 7 and y < 8:
                cell(x, y).set_step(x - y - 1)  # x - 8 + 7 - y
            elif x < 8 and y > 7:
                cell(x, y).set_step(y - x - 1)  # 7 - x + y - 8
            else:
                cell(x, y).set_step(x + y - 16)  # x - 8 + y - 8


def modified_flood():
    """ Specifically flood only relevant cells and not from center """
    flood_list = [[i, j]]
    while len(flood_list) != 0:
        x = flood_list[-1][0]
        y = flood_list[-1][1]
        flood_list.pop(-1)
        min_distance = 1000
        if not cell(x, y).north_wall:
            min_distance = cell(x, y+1).step

        if not cell(x, y).south_wall and cell(x, y-1).step < min_distance:
            min_distance = cell(x, y-1).step

        if not cell(x, y).east_wall and cell(x+1, y).step < min_distance:
            min_distance = cell(x+1, y).step

        if not cell(x, y).west_wall and cell(x-1, y).step < min_distance:
            min_distance = cell(x-1, y).step

        if cell(x, y).step != min_distance + 1:
            cell(x, y).set_step(min_distance + 1)
            if y < 15 and cell(x, y+1).step != 0 and [x, y+1] not in flood_list:
                flood_list.append([x, y+1])
            if y > 0 and cell(x, y-1).step != 0 and [x, y-1] not in flood_list:
                flood_list.append([x, y-1])
            if x < 15 and cell(x+1, y).step != 0 and [x+1, y] not in flood_list:
                flood_list.append([x+1, y])
            if x > 0 and cell(x-1, y).step != 0 and [x-1, y] not in flood_list:
                flood_list.append([x-1, y])


def reset():
    """ Reset the memory before traversing the maze"""
    global i, j, curr_north_wall, curr_south_wall, curr_west_wall,\
        curr_east_wall, require_flooding
    Maze.clear_mem()
    i = 0
    j = 0
    curr_north_wall = False
    curr_south_wall = True
    curr_west_wall = True
    curr_east_wall = True
    require_flooding = False
    cell(0, 0).set_checked(True)
    initial_flood()


def run_algorithm():
    """ The algorithm which is to be iterated until the center is reached """
    global i, j, require_flooding
    advance()
    if cell(i, j).step == 0:
        return "done"
    read_wall()
    if require_flooding:
        modified_flood()
    return "not done"

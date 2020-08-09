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
#     Last Modified: 8/8/2020
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
    return x, y


x, y = 0, 0  # record current position
require_flooding = False  # record if current update needs another flood
# initialize variables for current wall info, starts at (0, 0)
curr_north_wall = False
curr_south_wall = True
curr_west_wall = True
curr_east_wall = True


def read_wall():
    """ Read wall info, either by sensors, or from previous run
    If no new wall is found, no flooding is required """
    global curr_north_wall, curr_south_wall, curr_east_wall, curr_west_wall,\
        require_flooding
    curr_north_wall = sensor_cell(x, y).north_wall
    curr_south_wall = sensor_cell(x, y).south_wall
    curr_west_wall = sensor_cell(x, y).west_wall
    curr_east_wall = sensor_cell(x, y).east_wall
    require_flooding = False

    if cell(x, y).north_wall != curr_north_wall:
        require_flooding = True
        cell(x, y).set_north_wall(curr_north_wall)
        if y < 15:
            cell(x, y+1).set_south_wall(curr_north_wall)

    if cell(x, y).south_wall != curr_south_wall:
        require_flooding = True
        cell(x, y).set_south_wall(curr_south_wall)
        if y > 0:
            cell(x, y-1).set_north_wall(curr_south_wall)

    if cell(x, y).west_wall != curr_west_wall:
        require_flooding = True
        cell(x, y).set_west_wall(curr_west_wall)
        if x > 0:
            cell(x-1, y).set_east_wall(curr_west_wall)

    if cell(x, y).east_wall != curr_east_wall:
        require_flooding = True
        cell(x, y).set_east_wall(curr_east_wall)
        if x < 15:
            cell(x+1, y).set_west_wall(curr_east_wall)


def advance():
    """ Move to the next best path """
    global x, y
    shortest = 1000
    path = ""
    if y < 15 and not curr_north_wall:
        shortest = cell(x, y+1).step
        path = "n"
    if y > 0 and not curr_south_wall and cell(x, y-1).step < shortest:
        shortest = cell(x, y-1).step
        path = "s"
    if x < 15 and not curr_east_wall and cell(x+1, y).step < shortest:
        shortest = cell(x+1, y).step
        path = "e"
    if x > 0 and not curr_west_wall and cell(x-1, y).step < shortest:
        path = "w"

    if path == "n":  # advance north
        y += 1
    elif path == "s":  # advance south
        y -= 1
    elif path == "w":  # advance west
        x -= 1
    else:  # advance east
        x += 1
    cell(x, y).set_checked(True)


def initial_flood():
    """ Initially flood the maze with distances from center """
    for i in range(16):
        for j in range(16):
            if i < 8 and j < 8:
                cell(i, j).set_step(14 - i - j)  # 7 - x + 7 - y
            elif i > 7 and j < 8:
                cell(i, j).set_step(i - j - 1)  # x - 8 + 7 - y
            elif i < 8 and j > 7:
                cell(i, j).set_step(j - i - 1)  # 7 - x + y - 8
            else:
                cell(i, j).set_step(i + j - 16)  # x - 8 + y - 8


def modified_flood():
    """ Specifically flood only relevant cells and not from center """
    flood_list = [[x, y]]
    while len(flood_list) != 0:
        i = flood_list[-1][0]
        j = flood_list[-1][1]
        flood_list.pop(-1)
        min_distance = 1000
        if not cell(i, j).north_wall:
            min_distance = cell(i, j+1).step

        if not cell(i, j).south_wall and cell(i, j-1).step < min_distance:
            min_distance = cell(i, j-1).step

        if not cell(i, j).east_wall and cell(i+1, j).step < min_distance:
            min_distance = cell(i+1, j).step

        if not cell(i, j).west_wall and cell(i-1, j).step < min_distance:
            min_distance = cell(i-1, j).step

        if cell(i, j).step != min_distance + 1:
            cell(i, j).set_step(min_distance + 1)
            if j < 15 and cell(i, j+1).step != 0 and [i, j+1] not in flood_list:
                flood_list.append([i, j+1])
            if j > 0 and cell(i, j-1).step != 0 and [i, j-1] not in flood_list:
                flood_list.append([i, j-1])
            if i < 15 and cell(i+1, j).step != 0 and [i+1, j] not in flood_list:
                flood_list.append([i+1, j])
            if i > 0 and cell(i-1, j).step != 0 and [i-1, j] not in flood_list:
                flood_list.append([i-1, j])


def at_center():
    """ Determine if the robot has reached the center cells """
    return cell(x, y).step == 0


def reset():
    """ Reset the memory before traversing the maze"""
    global x, y, curr_north_wall, curr_south_wall, curr_west_wall,\
        curr_east_wall, require_flooding
    Maze.clear_mem()
    x = 0
    y = 0
    curr_north_wall = False
    curr_south_wall = True
    curr_west_wall = True
    curr_east_wall = True
    require_flooding = False
    cell(0, 0).set_checked(True)
    initial_flood()


def run_algorithm():
    """ The algorithm which is to be iterated until the center is reached """
    global x, y, require_flooding
    advance()
    if at_center():
        return "done"
    read_wall()
    if require_flooding:
        modified_flood()
    return "not done"

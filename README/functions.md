# Use ModifiedFloodFill.py for reference on how to use the available modules

class Cell:
    """ Class that represents a single cell """
    def __init__(self):
        self.checked = False
        self.north_wall = False
        self.south_wall = False
        self.west_wall = False
        self.east_wall = False
        self.step = 10
        self.int_var = 10
        self.bool_var = 10

    def set_checked(self, status: bool):
        """ Set this cell whether having been previously traversed or not """

    def set_north_wall(self, status: bool):
        """ Set the status of north wall of this cell as existing or not """

    def set_south_wall(self, status: bool):
        """ Set the status of south wall of this cell as existing or not """

    def set_west_wall(self, status: bool):
        """ Set the status of west wall of this cell as existing or not """

    def set_east_wall(self, status: bool):
        """ Set the status of east wall of this cell as existing or not """

    def set_step(self, val: int):
        """ Set the steps needed to get from the origin to this cell """

    def set_int_var(self, val: int):
        """ Set an additional integer variable if needed """

    def set_bool_var(self, status: bool):
        """ Set an additional boolean variable if needed """

class ParentMaze:
    """ Class to store mazes of different perspectives for the robot"""

    sensor_maze = [[Cell() for y in range(16)] for x in range(16)]
    maze = [[Cell() for y in range(16)] for x in range(16)]

    @classmethod
    def sensor_cell(cls, x, y):
        """ Return the cell of the actual maze at the given coordinate """

    @classmethod
    def cell(cls, x, y):
        """Return the cell of robot's virtual maze at the given coordinate"""

    @classmethod
    def print(cls):
        """ Print out robot's virtual maze in its
        current state to the console """

    @classmethod
    def sensor_print(cls):
        """ Print out the actual maze to the console """

    @classmethod
    def create(cls):
        """ Create a random organic maze """

    @classmethod
    def clear_mem(cls):
        """ Reset the mouse's memory of the virtual maze """


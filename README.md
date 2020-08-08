# Use RandomeGuessing.py for reference on how to use the available modules. For more advanced user, take a look at ModifiedFloodFill.py

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
        
- Micromouse is a robot whose ability is navigating through a maze autonomously
  without user input.
- This program allows the user to write and test their algorithms without the need
  of a physical micromouse.
- It also allows the user to create their own maze, save it, or retrieve later.
  Users can also pull maze from custom mode into normal mode to test their algorithms
  on the custom maze they created.

- "MOVEMENT" IN THIS APP IS SIMPLY A CHANGE OF THE COORDINATES.
- IMPORTANT: This app does NOT simulate physical movements, only the algorithm.
  I cannot stress this enough. If you ever wonder whether this app imitates
  certain movements or sensing of the real bot, it probably doesn't.

- Write your own algorithms by following the sample script BlankAlgorithm.py and
  the sample algorithms,  ModifiedFloodFill.py. Place your algorithm in the
  "algorithms" folder.
- Make your custom maze by clicking the Custom Mode button. Set up the walls for
  the maze by clicking on their positions on the big canvas. To save a maze, insert
  a name in the input box next to the Save Maze button, then click on the Save Maze
  button.


* Sample algorithms & application programmed by Cuong Nguyen, '23
* Modified floodfill algorithm developed by Prof. George Law, California State
    University, Northridge
* Maze generator programmed by Matt Burns, '20

Version History:
  - Micromouse App 2.0 7/6/2020: Restructured
  - Micromouse App 3.0 7/7/2020: Restructured and added the dropdown menu
  - Micromouse App 4.0 7/8/2020: Added position indicator
  - Micromouse App 4.1 7/9/2020: Initialized custom maze
  - Micromouse App 4.2 7/10/2020: Restructured and improved custom maze
  - Micromouse App 4.3 7/11/2020: Restructured and improved custom maze
  - Micromouse App 4.4 7/12/2020: Improved custom maze
  - Micromouse App 6.0 8/4/2020: End of Summer 2020 pre-release final Version
  - Micromosue App 7.0 8/7/2002: End of Summer 2020 final version

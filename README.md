In the words of Guido van Rossum (founder of Python):
> Code is read much more often than it is written
---
# **Introduction**
*   Micromouse is a robot whose ability is navigating autonomously through a maze without user input.
*   This program allows the user to write and test their algorithms without the need of a physical micromouse.
*   It also allows the user to create their own maze, save and retrieve it, and test their alogirthms on it.

# **User Guide**

###  I.   Movement
*   "Movement" in this app is simply a change of coordinates.
*   IMPORTANT: This app does NOT simulate physical movements, only the algorithm. I cannot stress this enough. If you ever wonder whether this app imitates certain movements of the real bot, it probably doesn't.

###  II.  Algorithm

Below are all available classes and functions

    ```
    class Cell:
    " Class that represents a single cell "
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
        " Set this cell whether having been previously traversed or not "

        def set_north_wall(self, status: bool):
        " Set the status of north wall of this cell as existing or not "

        def set_south_wall(self, status: bool):
        " Set the status of south wall of this cell as existing or not "

        def set_west_wall(self, status: bool):
        " Set the status of west wall of this cell as existing or not "

        def set_east_wall(self, status: bool):
        " Set the status of east wall of this cell as existing or not "

        def set_step(self, val: int):
        " Set the steps needed to get from the origin to this cell "

        def set_int_var(self, val: int):
        " Set an additional integer variable if needed "

        def set_bool_var(self, status: bool):
        " Set an additional boolean variable if needed "

    class ParentMaze:
    " Class to store mazes of different perspectives for the robot "

        sensor_maze = [[Cell() for y in range(16)] for x in range(16)]
        maze = [[Cell() for y in range(16)] for x in range(16)]

        @classmethod
        def sensor_cell(cls, x, y):
        " Return the cell of the actual maze at the given coordinate "

        @classmethod
        def cell(cls, x, y):
        " Return the cell of robot's virtual maze at the given coordinate "

        @classmethod
        def print(cls):
        " Print out robot's virtual maze in its current state to the console "

        @classmethod
        def sensor_print(cls):
        " Print out the actual maze to the console "

        @classmethod
        def create(cls):
        " Create a random organic maze "

        @classmethod
        def clear_mem(cls):
        " Reset the mouse's memory of the virtual maze "


    class Maze(ParentMaze):
    " Creating a child class of ParentMaze "

    def cell(x, y):
    " Return the cell of robot's virtual maze at the given coordinate "

    def sensor_cell(x, y):
    " Return the cell of the actual maze at the given coordinate "

    def create():
    " Create a random organic maze "

    def maze_print():
    " Print out robot's virtual maze in its current state to the console "

    def sensor_print():
    " Print out the actual maze to the console "

    x, y = 0, 0  # record current position

    def cur_pos():
    " Return the current position of the mouse "

    def at_center():
    " Determine if the robot has reached the center cells "

    def reset():
    " Reset the memory before traversing the maze "

    def run_algorithm():
    " The algorithm which is to be iterated until the center is reached
      Return "done" if the center is reached, return "not done" otherwise "
    ```
*   Write your own algorithms by making a copy of the sample script BlankAlgorithm.py. Make sure you also keep the copy in the "algorithms" folder. Make all your edits in this new copy. All functions and class included are required for compatibility with the apps. Refer to the comments in BlankAlgorithm.py for more details.
*   Refer to RandomGuessing.py as an example on how to use the available classes and functions if you're a beginner to the app. If you're a little more advanced, take a look at ModifiedFloodFill.py.
*   Description of RandomGuessing.py:
    *   'ParentMaze' module must be imported in every algorithm. Then create a child class `Maze` of `ParentMaze` with `class Maze(ParentMaze):`.
    *   There is usually no need to modify the subsequent functions `cell(x,y)`, `sensor_cell(x, y)`, `create()`, `maze_print()`, `sensor_print()`, and `cur_pos()`. It is not recommended that users do anything to these functions if they are still new to the app. Everything that comes after them is up to the user to program.
    *   `x, y` are used to store the current position of the robot in the maze. `at_center()` determines whether the bot has reached the center cells, meaning the algorithm has finished.
    *   `reset()` resets everything back as if the bot has just been put down at (0, 0). This function is used by the app to reset the mouse before starting another navigation.
    *   `run_algorithm()` makes the mouse move "one step" (one step of the algorithm, not necessarily exactly one coordinate/cell). First, `run_algorithm()` checks if the bot has reached the center by returning `"done"`so it stops navigating. Next, the mouse checks the surrounding walls, and add the open paths to `choices`. Then, the mouse removes the path that is supposedly at the back of the mouse by checking its `previous_choice`. *NOTE: this is not needed in a real bot, because the bot literally doesn't have a sensor in the back to check if that path is open. And users can just not use the moving backward function.* Then, `random.choice(choices)` picks a random option out of `choices`. Then, it changes the coordinate according to the selection. Add 1 to `y` if selected `path` is north, and likewise. Then, `cell(x, y).set_checked(True)` sets this new position as being checked. Make sure to return `"not done"` at the end of this `run_algorithm()` function.
    *   There are other properties of a cell too such as `step`, `int_var`, and `bool_var`. Use them as you see fit.
    * To change the algorithm for navigation, click on the dropdown menu at the top right of the window next to the text *Select your algorithm* and select your desired one. The default selection is ModifiedFloodFill.py

###  II.  Large Maze (big canvas)
*   Display the newly generated mazes.
*   During the mouse's navigation, display everything that the mouse knows about the maze.
*   While in Custom Mode, users can create their maze by clicking on the dashed lines on this big canvas.

###  III. Small Maze (small canvas)
*   There is a small italic text above this small canvas that states which maze the small canvas is displaying.
*   While in normal mode, display what would be on the big canvas if users go into custom mode. In other words, it displays the custom maze.
*   While in custom mode, display what would be on the big canvas if users go into normal mode. In other words, it displays the generated maze.
*   During the mouse's navigation, it displays the whole maze which the mouse is traversing in. Not important to the mouse, this is only for user's reference.

###  IV. Navigation Options
*   Click on Start Navigation to run the selected algorithm on the maze currently being displayed on the big canvas.
*   If the Show numbers box is checked, the navigation will display the `step` property of each cell, with the traversed cells being colored yellow. If not, "x" letters will be marked along the traversed path, with the current position being marked with a diamond shape.
*   If the Show individual steps box is checked, the app will display each movement of the mouse. Otherwise, it will simply display the final result.
*   The Generate New Maze button will generate a new random maze.
*   To transfer the maze from custom mode into normal mode, click on Rollover Custom.
*   Use the Movement Delay slider to speed up or slow down the navigation speed.

###  V. Custom Mode Options
*   Enter the Custom Mode by clicking the Custom Mode button.
*   Set up the walls for the maze by clicking on their positions on the big canvas. Sometimes, the app will ignore your click, if the cursor's position is too close to two different walls simultaneously or if the cursor's position is too far from a wall.
*   To save a maze, insert a name in the input box next to the Save Maze button, then click on the Save Maze button.
*   To open a saved maze, click on the Retrieve Maze button. It will open a file dialog, then choose the maze that you want. Enable the Preview Pane in the file dialog if you're not sure which name you saved the maze under.
*   Users can also transfer the generated maze from normal mode over by clicking on Rollover Generated.
*   IMPORTANT: NEVER open these maze files outside of the app to edit them. You can overwrite these files from within the app. FYI, the maze you see on the preview pane, or when you open these files is of no importance to the app. That's for user's reference. What's important is the long line of characters at the bottom of the files.

# **Credits**
*   Sample algorithms & application programmed by Cuong Nguyen, '23, University of Scranton
*   Modified floodfill algorithm developed by Prof. George Law, California State University, Northridge (PowerPoint explanation can be found online)
*   Maze generator programmed by Matt Burns, '20, University of Scranton
*   Tested by Ryan Chan, '23, Cornell University
*   Mouse icon and diamond icon made by [Freepik](https://www.freepik.com/) from [www.flaticon.com](https:///www.flaticon.com/) 

# **Version History**
*   Micromouse App 2.0 7-6-2020: Restructured
*   Micromouse App 3.0 7-7-2020: Restructured and added the dropdown menu
*   Micromouse App 4.0 7-8-2020: Added position indicator
*   Micromouse App 4.1 7-9-2020: Initialized custom maze
*   Micromouse App 4.2 7-10-2020: Restructured and improved custom maze
*   Micromouse App 4.3 7-11-2020: Restructured and improved custom maze
*   Micromouse App 4.4 7-12-2020: Improved custom maze
*   Micromouse App 5.0 8-4-2020: End of Summer 2020 pre-release final version
*   Micromosue App 5.1 8-8-2020: End of Summer 2020 final version

# **Contact**
Feedback and feature requests are always welcomed. Please direct them to cuong.nguyen@scranton.edu

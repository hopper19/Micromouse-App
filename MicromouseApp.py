"""
# ----------------------------------------------------------------------------
#     Name: MicromouseApp.py
#     Purpose: App to demonstrate how different algorithms work
#
#     Author: CUONG NGUYEN
#
#     Last Modified: 8/4/2020
# ----------------------------------------------------------------------------
"""
from tkinter import Tk, Button, Canvas, Checkbutton, IntVar, StringVar,\
    OptionMenu, Label, PhotoImage, filedialog, Entry, messagebox, Frame
import sys
sys.path.append("./algorithms")
from CellMod import Cell
from os import listdir
from os.path import isfile, join
imports = [f for f in listdir("./algorithms") if isfile(join("./algorithms", f))]
imports.remove("CellMod.py")
imports.remove("MazeMod.py")
for m in range(len(imports)):
    dot_index = imports[m].find(".")
    imports[m] = imports[m].replace(imports[m][dot_index:len(imports[m])], "")
algorithms = []
for n in imports:
    algorithms.append(__import__(n))


class MazeConfig:
    """ Class to store custom maze """
    def __init__(self):
        self.sensor_maze = [[Cell() for y in range(16)] for x in range(16)]
        for i in range(16):
            self.sensor_maze[i][0].set_south_wall(True)
            self.sensor_maze[0][i].set_west_wall(True)
            self.sensor_maze[i][15].set_north_wall(True)
            self.sensor_maze[15][i].set_east_wall(True)
        self.sensor_maze[0][0].set_east_wall(True)
        self.sensor_maze[1][0].set_west_wall(True)

    def sensor_cell(self, x: int, y: int):
        """ Return the cell of the actual maze at the given coordinate """
        return self.sensor_maze[x][y]

    def sensor_print(self):
        """ Print out the actual maze to the console """
        print("+", end="")
        for j in range(16):
            print("----+", end="")
        print()
        for j in reversed(range(16)):
            print("|", end="")
            for i in range(16):
                print("    ", end="")
                if self.sensor_maze[i][j].east_wall:
                    print("|", end="")
                else:
                    print(" ", end="")
            print()
            print("+", end="")
            for i in range(16):
                if self.sensor_maze[i][j].south_wall:
                    print("----+", end="")
                else:
                    print("    +", end="")
            print()

    def print_to_file(self, file):
        """ Print the custom maze to the txt file for preview """
        file.write("+")
        for j in range(16):
            file.write("--+")
        file.write("\n")
        for j in reversed(range(16)):
            file.write("|")
            for i in range(16):
                file.write("  ")
                if self.sensor_maze[i][j].east_wall:
                    file.write("|")
                else:
                    file.write(" ")
            file.write("\n+")
            for i in range(16):
                if self.sensor_maze[i][j].south_wall:
                    file.write("--+")
                else:
                    file.write("  +")
            file.write("\n")


def start_navigation():
    """ Start the navigation of the virtual mouse through the created maze """
    draw_side("generated")
    reset()
    if step_input.get():
    # disable some buttons to avoid functions overriding each other
        generate_button.config(state="disabled")
        algorithm_menu.config(state="disabled")
        custom_button.config(state="disabled")
        rollover_custom.config(state="disabled")
        start_button.config(text="Restart Navigation")
    side_label.config(text="Displaying original canvas maze...")
    iteration_count = 0
    while run_algorithm() != "done":
        iteration_count += 1
        if iteration_count == 512:
        # if the algorithm iterates for more than 512 times, declare it's unsolvable
        # due to either the maze is unsolvable or the algorithm failed to solve it
            start_button.config(text="Unsolvable", state="disabled")
            break
        if number_input.get():
            show_number.config(text="Uncheck for position")
        else:
            show_number.config(text="Show numbers")
        if step_input.get():
            canvas.after(500, draw_maze("virtual"))
    # set buttons back to active
    generate_button.config(state="normal")
    algorithm_menu.config(state="normal")
    custom_button.config(state="normal")
    rollover_custom.config(state="normal")
    if iteration_count != 512:
        start_button.config(text="Start Navigation")
    if number_input.get():
        show_number.config(text="Uncheck for position")
    else:
        show_number.config(text="Show numbers")
    show_step.config(text="Show individual steps")
    draw_maze("virtual")  # draw the final result


def generate_maze():
    """ Generate and display a new maze """
    if start_button.cget("text") == "Unsolvable":
    # reactivate the start button after a new maze is generated
        start_button.config(text="Start Navigation", state="normal")
    maze_create()
    draw_maze("real")


def save_maze():
    """ Save the custom created maze """
    if input_box.get() == "":
    # do nothing if user didn't insert a file name
        messagebox.showinfo("Alert!", "No name was provided")
    else:
        maze_bin = ""
        maze_file = open("./mazes/" + input_box.get() + ".txt", "w")
        maze_config.print_to_file(maze_file)
        # record north wall and west wall as one big binary number
        for j in reversed(range(16)):
            for i in range(16):
                if maze_config.sensor_cell(i, j).north_wall:
                    maze_bin += "1"
                else:
                    maze_bin += "0"
            for i in range(16):
                if maze_config.sensor_cell(i, j).west_wall:
                    maze_bin += "1"
                else:
                    maze_bin += "0"
        # convert the binary number into hexadecimal and write it to the file
        maze_file.write(hex(int(maze_bin, 2)))
        maze_file.close()
        if "pearson" in input_box.get().lower():
            scranton_prep = PhotoImage(file="images/SP.png")
            side_canvas.create_image(163, 163, image=scranton_prep)
            side_canvas.update()
            side_canvas.after(120)


def retrieve_maze():
    """ Retrieve the saved custom maze """
    # open a file dialog for user to open a maze config
    window.filename = filedialog.askopenfilename(initialdir="./mazes",
        title="Select a Maze Configuration")
    if window.filename != "":
    # do nothing if user has selected nothing.
    # Without this, it would cause an exception
        maze_file = open(window.filename, "r")
        maze_hex = ""
        for maze_hex in maze_file:  # get only the last line in the file
            pass
        maze_bin = bin(int(maze_hex, 16)).lstrip("0b")  # conver hex to binary
        maze_file.close()
        # reconstruct the maze config
        for j in reversed(range(16)):
            maze_config.sensor_cell(j, 0).set_south_wall(True)
            maze_config.sensor_cell(15, j).set_east_wall(True)
            for i in range(16):
                maze_config.sensor_cell(i, j).set_north_wall(int(maze_bin[0]))
                maze_bin = maze_bin[1:]
                if j != 15:
                    maze_config.sensor_cell(i, j+1).set_south_wall(maze_config.sensor_cell(i, j).north_wall)
            for i in range(16):
                maze_config.sensor_cell(i, j).set_west_wall(int(maze_bin[0]))
                maze_bin = maze_bin[1:]
                if i != 0:
                    maze_config.sensor_cell(i-1, j).set_east_wall(maze_config.sensor_cell(i, j).west_wall)
        draw_custom_maze()


def custom_maze_mode():
    """ Enter custom mode when the custom button is pressed """
    if custom_button.cget("text") == "Custom Mode":
        # when custom mode, hide all other buttons
        canvas.bind("<Button-1>", click)
        algorithm_frame.grid_forget()
        navigation_frame.grid_forget()
        rollover_generated.grid(row=1, column=0, columnspan=2, ipadx=5, pady=3)
        clear_button.grid(row=2, column=0, columnspan=2, ipadx=72, pady=3)
        retrieve_button.grid(row=3, column=0, columnspan=2, ipadx=30, pady=3)
        input_box.grid(row=4, column=0, ipady=5, pady=3)
        save_button.grid(row=4, column=1, ipadx=5, pady=3)
        custom_button.config(text="Done!", background=LIGHT_GREEN,
            activebackground=GREEN)
        side_label.config(text="Displaying generated maze...")
        draw_side("generated")
        draw_custom_maze()
    else:
        # hide the custom buttons and
        # set everything else back to normal after clicking "Done!"
        canvas.unbind("<Button-1>")
        algorithm_frame.grid(row=0, column=1, columnspan=2)
        navigation_frame.grid(row=5, column=1, columnspan=2, rowspan=3)
        rollover_generated.grid_forget()
        clear_button.grid_forget()
        retrieve_button.grid_forget()
        input_box.grid_forget()
        save_button.grid_forget()
        custom_button.config(text="Custom Mode", background=LIGHT_GREY,
            activebackground=GREY)
        side_label.config(text="Displaying custom maze...")
        draw_side("custom")
        draw_maze("real")


def click(event):
    """ Events that would happen if the canvas is clicked in custom mode """
    # get the coordinates of the wall which is closest to where cursor pressed
    x = (event.x - 3)//50
    y = (797 - event.y)//50
    if x < 0 or x > 15 or y < 0 or y > 15:  # discard if coors out of bound
        return
    # get the decimal part of the calculation
    # (discard the coordinates if the error is outside of allowed margin)
    x_diff = round((event.x - 3)/50, 2) - x
    y_diff = round(16 - (event.y-3)/50, 2) - y
    if x_diff > 0.75:
        if y_diff > 0.8 or y_diff < 0.2:
            return
        elif x != 15:
            maze_config.sensor_cell(x, y).set_east_wall(not maze_config.sensor_cell(x, y).east_wall)
            maze_config.sensor_cell(x+1, y).set_west_wall(not maze_config.sensor_cell(x+1, y).west_wall)
    elif x_diff < 0.25:
        if y_diff > 0.8 or y_diff < 0.2:
            return
        elif x != 0:
            maze_config.sensor_cell(x, y).set_west_wall(not maze_config.sensor_cell(x, y).west_wall)
            maze_config.sensor_cell(x-1, y).set_east_wall(not maze_config.sensor_cell(x-1, y).east_wall)
    elif y_diff > 0.75:
        if x_diff > 0.8 or x_diff < 0.2:
            return
        elif y != 15:
            maze_config.sensor_cell(x, y).set_north_wall(not maze_config.sensor_cell(x, y).north_wall)
            maze_config.sensor_cell(x, y+1).set_south_wall(not maze_config.sensor_cell(x, y+1).south_wall)
    elif y_diff < 0.25:
        if x_diff > 0.8 or x_diff < 0.2:
            return
        elif y != 0:
            maze_config.sensor_cell(x, y).set_south_wall(not maze_config.sensor_cell(x, y).south_wall)
            maze_config.sensor_cell(x, y-1).set_north_wall(not maze_config.sensor_cell(x, y-1).north_wall)
    # redraw the custom maze after new logical position has been updated
    draw_custom_maze()


def draw_maze(maze):
    """ Display the maze being passed """
    # real for the actual maze, virtual for what the mouse currently knows
    canvas.delete("all")
    for i in range(17):
        for j in range(17):
            canvas.create_rectangle(j*50 + 2, i*50 + 2, j*50 + 7, i*50 + 7,
                fill=RED, outline="")
    for i in range(16):
        canvas.create_line(i*50 + 5, 804, i*50 + 55, 804, fill=RED, width=5)
        canvas.create_line(804, i*50 + 5, 804, i*50 + 55, fill=RED, width=5)
        if maze == "virtual":
            canvas.create_line(i*50 + 5, 4, i*50 + 55, 4, fill=RED, width=5)
            canvas.create_line(4, i*50 + 5, 4, i*50 + 55, fill=RED, width=5)
        for j in range(16):
            if maze == "real":
            # print all the walls of the maze
                if sensor_cell(i, j).north_wall:
                    canvas.create_line(i*50 + 5, 754 - j*50, i*50 + 55, 754 - j*50,
                        fill=RED, width=5)
                if sensor_cell(i, j).west_wall:
                    canvas.create_line(i*50 + 4, 755 - j*50, i*50 + 4, 805 - j*50,
                        fill=RED, width=5)
            else:
            # only print the walls that the bot has observed
                if cell(i, j).north_wall:
                    canvas.create_line(i*50 + 5, 754 - j*50, i*50 + 55, 754 - j*50,
                        fill=RED, width=5)
                if cell(i, j).west_wall:
                    canvas.create_line(i*50 + 4, 755 - j*50, i*50 + 4, 805 - j*50,
                        fill=RED, width=5)
                if number_input.get():
                    if cell(i, j).checked:
                        canvas.create_text(i*50 + 30, 779 - j*50, text=cell(i, j).step,
                            fill=YELLOW, font=("arial", 12, "bold"))
                    else:
                        canvas.create_text(i*50 + 30, 779 - j*50, text=cell(i, j).step,
                            fill=WHITE, font=("arial", 12, "bold"))
    if not number_input.get() and maze == "virtual":
    # mark the travelled path, diamond for the current position
        diamond = PhotoImage(file="images/diamond.png")
        for i in range(16):
            for j in range(16):
                if cell(i, j).checked:
                    canvas.create_text(i*50 + 30, 779 - j*50, text="x",
                        fill=YELLOW, font=("arial", 12, "bold"))
                if (i, j) == cur_pos():
                    canvas.create_image(i*50 + 31, 781 - j*50, image=diamond)
    canvas.update()


def draw_custom_maze():
    """ Draw maze created from custom mode """
    canvas.delete("all")
    for i in range(16):
        canvas.create_line(i*50 + 5, 804, i*50 + 55, 804, fill=RED, width=5)
        canvas.create_line(804, i*50 + 5, 804, i*50 + 55, fill=RED, width=5)
        for j in range(16):
            if maze_config.sensor_cell(i, j).north_wall:
                canvas.create_line(i*50 + 5, 754 - j*50, i*50 + 55, 754 - j*50,
                    fill=RED, width=5)
            elif custom_button.cget("text") != "Custom Mode":
                canvas.create_line(i*50 + 5, 754 - j*50, i*50 + 55, 754 - j*50,
                    fill=DARK_GREY, dash=(3, 3))
            if maze_config.sensor_cell(i, j).west_wall:
                canvas.create_line(i*50 + 4, 755 - j*50, i*50 + 4, 805 - j*50,
                    fill=RED, width=5)
            elif custom_button.cget("text") != "Custom Mode":
                canvas.create_line(i*50 + 4, 755 - j*50, i*50 + 4, 805 - j*50,
                    fill=DARK_GREY, dash=(3, 3))
    for i in range(17):
        for j in range(17):
            canvas.create_rectangle(j*50 + 2, i*50 + 2, j*50 + 7, i*50 + 7,
                fill=RED, outline="")
    canvas.update()


def draw_side(maze):
    """ Draw the custom maze on the side canvas """
    side_canvas.delete("all")
    for i in range(17):
        for j in range(17):
            side_canvas.create_rectangle(j*20 + 2, i*20 + 2, j*20 + 5, i*20 + 5,
                fill=RED, outline="")
    for i in range(16):
        side_canvas.create_line(i*20 + 4, 320, i*20 + 24, 320, fill=RED, width=3)
        side_canvas.create_line(320, i*20 + 4, 320, i*20 + 24, fill=RED, width=3)
        for j in range(16):
            if (maze == "custom" and maze_config.sensor_cell(i, j).north_wall) or\
                (maze == "generated" and sensor_cell(i, j).north_wall):
                side_canvas.create_line(i*20 + 4, 303 - j*20, i*20 + 24, 303 - j*20,
                    fill=RED, width=3)
            if (maze == "custom" and maze_config.sensor_cell(i, j).west_wall) or\
                (maze == "generated" and sensor_cell(i, j).west_wall):
                side_canvas.create_line(i*20 + 3, 304 - j*20, i*20 + 3, 324 - j*20,
                    fill=RED, width=3)
    side_canvas.update()


def clear_custom():
    """ Clear the custom maze """
    for i in range(16):
        for j in range(16):
            maze_config.sensor_cell(i, j).set_north_wall(False)
            maze_config.sensor_cell(i, j).set_south_wall(False)
            maze_config.sensor_cell(i, j).set_west_wall(False)
            maze_config.sensor_cell(i, j).set_east_wall(False)
    for i in range(16):
        maze_config.sensor_cell(i, 0).set_south_wall(True)
        maze_config.sensor_cell(0, i).set_west_wall(True)
        maze_config.sensor_cell(i, 15).set_north_wall(True)
        maze_config.sensor_cell(15, i).set_east_wall(True)
    maze_config.sensor_cell(0, 0).set_east_wall(True)
    maze_config.sensor_cell(1, 0).set_west_wall(True)
    draw_custom_maze()


def assign_custom_maze():
    """ Copy generated maze into custom maze mode """
    for i in range(16):
        for j in range(16):
            maze_config.sensor_cell(i, j).set_north_wall(sensor_cell(i, j).north_wall)
            maze_config.sensor_cell(i, j).set_south_wall(sensor_cell(i, j).south_wall)
            maze_config.sensor_cell(i, j).set_west_wall(sensor_cell(i, j).west_wall)
            maze_config.sensor_cell(i, j).set_east_wall(sensor_cell(i, j).east_wall)
    draw_custom_maze()


def get_custom_maze():
    """ Copy custom maze into generated canvas """
    if start_button.cget("text") == "Unsolvable":
    # reactivate the start button if it was previously deactivated
        start_button.config(text="Start Navigation", state="normal")
    for i in range(16):
        for j in range(16):
            sensor_cell(i, j).set_north_wall(maze_config.sensor_cell(i, j).north_wall)
            sensor_cell(i, j).set_south_wall(maze_config.sensor_cell(i, j).south_wall)
            sensor_cell(i, j).set_west_wall(maze_config.sensor_cell(i, j).west_wall)
            sensor_cell(i, j).set_east_wall(maze_config.sensor_cell(i, j).east_wall)
    draw_maze("real")


def reset():
    """ Run the reset function from the respective selected algorithm """
    algorithms[imports.index(algorithm_selection.get())].reset()


def maze_create():
    """ Run the maze_create function from the respective selected algorithm """
    algorithms[imports.index(algorithm_selection.get())].create()


def run_algorithm():
    """ Run the run_algorithm function from the respective selected algorithm """
    return algorithms[imports.index(algorithm_selection.get())].run_algorithm()


def cell(x, y):
    """ Run the cell function from the respective selected algorithm """
    return algorithms[imports.index(algorithm_selection.get())].cell(x, y)


def sensor_cell(x, y):
    """ Run the sensor_cell function from the respective selected algorithm """
    return algorithms[imports.index(algorithm_selection.get())].sensor_cell(x, y)


def cur_pos():
    """ Run the cur_pos function from the respective selected algorithm """
    return algorithms[imports.index(algorithm_selection.get())].cur_pos()


# Miscellaneous variables
WHITE = "#FFFFFF"
YELLOW = "#FFFF00"
RED = "#FF0000"
BLACK = "#000000"
DARK_GREY = "#323232"
GREY = "#808080"
LIGHT_GREY = "#9a9a9a"
LIGHT_GREEN = "#00eb00"
GREEN = "#00c400"
maze_config = MazeConfig()

# Initialize the main window
window = Tk()
window.iconbitmap("images/mouse.ico")
window.state("zoomed")
window.title("Micromouse Algorithm Demonstrator")

# Add the canvases
canvas = Canvas(window, width=805, height=805, background=BLACK)
canvas.grid(row=0, column=0, rowspan=16)
side_canvas = Canvas(window, width=320, height=320, background=BLACK)
side_canvas.grid(row=10, column=1, rowspan=6, columnspan=2, padx=25)

# Add the algorithm menu
algorithm_frame = Frame(window)
algorithm_frame.grid(row=0, column=1, columnspan=2)
algorithm_label = Label(algorithm_frame, text="Select your algorithm:", font=("arial", 12, "bold"))
algorithm_label.grid(row=0, column=0)
algorithm_selection = StringVar()
algorithm_selection.set(imports[1])  # set default algorithm
algorithm_menu = OptionMenu(algorithm_frame, algorithm_selection, *imports)
algorithm_menu.config(background=LIGHT_GREY, border=0, cursor="hand2",
    activebackground=GREY, font=("arial", 13, "bold"))
algorithm_menu.grid(row=0, column=1, ipadx=5, ipady=5)

# Add frame for displaying navigation buttons
navigation_frame = Frame(window)
navigation_frame.grid(row=5, column=1, columnspan=2, rowspan=3)

# Add options for maze displaying
number_input = IntVar()
show_number = Checkbutton(navigation_frame, text="Show numbers", cursor="hand2",
    font=("arial", 12, "bold"), variable=number_input)
show_number.grid(row=0, column=0)
step_input = IntVar()
show_step = Checkbutton(navigation_frame, text="Show individual steps", cursor="hand2",
    variable=step_input, font=("arial", 12, "bold"))
show_step.grid(row=0, column=1)
show_step.select()

# Add main function buttons
start_button = Button(navigation_frame, text="Start Navigation", background=LIGHT_GREY,
    border=0, cursor="hand2", activebackground=GREY, font=("arial", 13, "bold"),
    command=start_navigation)
start_button.grid(row=1, column=0, ipadx=5, ipady=5, pady=7)
generate_button = Button(navigation_frame, text="Generate New Maze", background=LIGHT_GREY,
    border=0, cursor="hand2", activebackground=GREY, font=("arial", 13, "bold"),
    command=generate_maze)
generate_button.grid(row=1, column=1, ipadx=5, ipady=5, pady=7)
rollover_custom = Button(navigation_frame, text="Rollover Custom", background=LIGHT_GREY,
    border=0, cursor="hand2", activebackground=GREY, font=("arial", 13, "bold"),
    command=get_custom_maze)
rollover_custom.grid(row=2, column=0, columnspan=2, ipadx=5, ipady=5)
side_label = Label(window, text="Displaying custom maze...", font=("arial", 10, "italic"))
side_label.grid(row=9, column=1, columnspan=2)

# Add buttons for custom mode
custom_frame = Frame(window)
custom_frame.grid(row=1, column=1, columnspan=2, rowspan=5)
custom_button = Button(custom_frame, text="Custom Mode", background=LIGHT_GREY,
    border=0, cursor="hand2", activebackground=GREY, font=("arial", 15, "bold"),
    command=custom_maze_mode)
custom_button.grid(row=0, column=0, columnspan=2, ipadx=30, ipady=2, pady=5)
retrieve_button = Button(custom_frame, text="Retrieve Maze", background=LIGHT_GREY,
    border=0, cursor="hand2", activebackground=GREY, font=("arial", 15, "bold"),
    command=retrieve_maze)
rollover_generated = Button(custom_frame, text="Rollover Generated", background=LIGHT_GREY,
    border=0, cursor="hand2", activebackground=GREY, font=("arial", 15, "bold"),
    command=assign_custom_maze)
clear_button = Button(custom_frame, text="Clear", background=LIGHT_GREY,
    border=0, cursor="hand2", activebackground=GREY, font=("arial", 15, "bold"),
    command=clear_custom)
save_button = Button(custom_frame, text="Save Maze", background=LIGHT_GREY,
    border=0, cursor="hand2", activebackground=GREY, font=("arial", 13, "bold"),
    command=save_maze)
input_box = Entry(custom_frame, width=20)


""" Start the app """
maze_create()
draw_maze("real")
draw_side("custom")
window.mainloop()

#region VEXcode Generated Robot Configuration
import math
import random
from vexcode_vr import *

# Brain should be defined by default
brain=Brain()

drivetrain = Drivetrain("drivetrain", 0)
pen = Pen("pen", 8)
pen.set_pen_width(THIN)
left_bumper = Bumper("leftBumper", 2)
right_bumper = Bumper("rightBumper", 3)
front_eye = EyeSensor("frontEye", 4)
down_eye = EyeSensor("downEye", 5)
front_distance = Distance("frontdistance", 6)
distance = front_distance
magnet = Electromagnet("magnet", 7)
location = Location("location", 9)

#endregion VEXcode Generated Robot Configuration
myVariable = 0

def main():

    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.set_turn_velocity(100, PERCENT)
    drivetrain.set_heading(0, DEGREES)

    pen.set_pen_color(BLACK)
    pen.move(DOWN)

# gets the starting point

    row, col = get_cell()
    Visited[row + Offset][col + Offset] = True
    Path.append((row, col))

    while not down_eye.detect(RED):

        move()
        wait(0.1, SECONDS)

        # prints the coordinates of each move to the console
        
        row, col = get_cell()
        brain.print("\n")
        brain.print(row)
        brain.print(",")
        brain.print(col)

    Start = Path[0]
    End = Path[-1]

    Shortest_Path = BFS(Start, End)
# changes color to show the quickest route
    pen.move(UP)
    pen.set_pen_color(GREEN)
    pen.move(DOWN)
    
    drivetrain.set_heading(0, DEGREES)

    Follow_Path(Shortest_Path[::-1])





Step_MM = 250
Grid_Size = Step_MM
Size = 64
Offset = 15
Visited = [[False for _ in range(Size)] for _ in range(Size)]
Path = []

# finds valid directions to move using distance infront

def get_distance():
    # Front
    forward_move = distance.get_distance(MM) > Step_MM

    # Left
    drivetrain.turn_for(LEFT, 90, DEGREES)
    left_move = distance.get_distance(MM) > Step_MM

    # Right
    drivetrain.turn_for(LEFT, 180, DEGREES)
    right_move = distance.get_distance(MM) > Step_MM

    # Return to forward
    drivetrain.turn_for(LEFT, 90, DEGREES)

    return left_move, forward_move, right_move


# chooses which direction to move favouring left 
def move():
    left_move, forward_move, right_move = get_distance()
    # Left
    if left_move:
        drivetrain.turn_for(LEFT, 90, DEGREES)
        drivetrain.drive_for(FORWARD, Step_MM, MM)
    # Forward
    elif forward_move:
        drivetrain.drive_for(FORWARD, Step_MM, MM)
    # Right
    elif right_move:
        drivetrain.turn_for(RIGHT, 90, DEGREES)
        drivetrain.drive_for(FORWARD, Step_MM, MM)
    # Backward
    else:
        drivetrain.turn_for(RIGHT, 180, DEGREES)

    row, col = get_cell()
    Visited[row + Offset][col + Offset] = True
    Path.append((row, col))

# get the location of each move as coordinates

def get_cell():
    x = location.position(X, MM)
    y = location.position(Y, MM)

    col = round(x / Grid_Size)
    row = round(y / Grid_Size)

    return row, col

# BFS to find the quickest route of the maze
def BFS(Start, End):
    from collections import deque

    queue = deque([Start])
    Came_From = {Start: None}

    while queue:
        Current = queue.popleft()

        if Current == End:
            break
        row, col = Current

        Next_Squares = []
        for i in range(len(Path) - 1):
             if Path[i] == Current:
                 Next_Squares.append(Path[i+1])
             if Path[i+1] == Current:
                Next_Squares.append(Path[i])

        for Next_row, Next_col in Next_Squares:
            Grid_row = Next_row + Offset
            Grid_col = Next_col + Offset

            if Grid_row < 0 or Grid_row >= Size or Grid_col < 0 or Grid_col >= Size:
                continue

            if Visited[Grid_row][Grid_col] and (Next_row, Next_col) not in Came_From:
                queue.append((Next_row, Next_col))
                Came_From[(Next_row, Next_col)] = Current

    Shortest_Path = []
    Step = End

    while Step is not None:
        Shortest_Path.append(Step)
        Step = Came_From.get(Step)

    Shortest_Path.reverse()
    return Shortest_Path

#return home function using the quickest route

def Follow_Path(Shortest_Path):
    for i in range(len(Shortest_Path) - 1):

        Current_row, Current_col = Shortest_Path[i]
        Next_row, Next_col = Shortest_Path[i + 1]

        Row_Diff = Next_row - Current_row
        Col_Diff = Next_col - Current_col

         # north
        if Row_Diff == -1:
            drivetrain.turn_to_heading(90, DEGREES)

        # south
        elif Row_Diff == 1:
            drivetrain.turn_to_heading(270, DEGREES)

        # west
        elif Col_Diff == -1:
            drivetrain.turn_to_heading(180, DEGREES)

        # east
        elif Col_Diff == 1:
            drivetrain.turn_to_heading(0, DEGREES)

        drivetrain.drive_for(FORWARD, Step_MM, MM)


vr_thread(main)


     


    




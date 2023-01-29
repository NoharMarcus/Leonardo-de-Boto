"""
This is the main loop of De-Boto.
This is the page that connects all the components into one, big, happy, working, De-Boto :)
"""

# Regular Dependencies
from pickle import TRUE
import numpy as np

# Memory Management

# Helpers
import helpers.lut_artificial as lut_artificial

# Coordinates to Rotors Angels
import calculations.Calculator as Calculator

# converting img to angles
import helpers.tcp_send as tcp_send

# Converting img to x,y vectors
import lines.linedraw as linedraw

# LPF
import helpers.lpf as lpf

debug = False
# -----------------------Convert linedraw reigon ------------------------------------------------
def normalize_size_linedraw(lines, visualize=True):
    """
    :param lines: the lines as they get from linedraw
    :param drawing_area: build like this : [[min-x, max-x],[min-y, max-y]]
                         such that the x represent the desired x range (and vice versa)
    :param visualize: bool param for whether or not to visualize the new lines
    :return: new_lines: such that all the coords within are placed in the drawable area
    """

    # find the current coordinates bounderies
    max_x = 0
    min_x = 0
    max_y = 0
    min_y = 0

    for line in lines:
        for coord in line:
            max_x = max(max_x, coord[0])
            min_x = min(min_x, coord[0])
            max_y = max(max_y, coord[1])
            min_y = min(min_y, coord[1])

    width = max_x - min_x
    height = max_y - min_y

    # find the desired drawing range
    drawing_area, spin, y_offset = lut_artificial.find_image_bounderies([width, height])
    [desired_min_x, desired_max_x], [desired_min_y, desired_max_y] = drawing_area 

    # create new lines that are not based on tupel
    new_lines = []
    new_lines__round = []

    for line in lines:
        new_line = []
        new_line__round = []
        for coord in line:
            print()
            # normalize to [0,1]
            coord_x_normalised = (coord[0] - min_x) / (max_x - min_x)
            coord_y_normalised = (coord[1] - min_y) / (max_y - min_y)

            # normalize to given drawing_area
            new_x = (coord_x_normalised * (desired_max_x - desired_min_x)) + desired_min_x
            new_y = (coord_y_normalised * (desired_max_y - desired_min_y)) + desired_min_y

            # adding the updated coordinate to the new_line vector
            if (False): 
                # spin is a 90 degrees rotation of the img, (so it would fit the drawing area).
                # a 90 degrees rotation is replacing the x-axis and the y-axis
                new_line.append([new_y, new_x])
                new_line__round.append([round(new_y), round(new_x)])
            else:
                new_line.append([new_x, new_y])
                new_line__round.append([round(new_x), round(new_y)])

        #appending the updated line to the new_lines vector
        new_lines.append(new_line)
        new_lines__round.append(new_line__round)

    # make sure the range changed accordingly to the desired one.
    max_x = -3000
    min_x = 3000
    max_y = -3000
    min_y = 3000

    for line in new_lines:
        for coord in line:
            max_x = max(max_x, coord[0])
            min_x = min(min_x, coord[0])
            max_y = max(max_y, coord[1])
            min_y = min(min_y, coord[1])

    # if you want a live visual representation of the robot orders,
    # draw the lines in order using turtle graphics.
    if visualize:
        linedraw.visualize(lines)
        # linedraw.visualize(new_lines__round)
        # linedraw.visualize(new_lines)
        # show the picture dots on top of the feasible drawing area, and the page boundaries
        lut_artificial.show_lines_in_lut(new_lines__round, y_offset)
        
    return new_lines
# -----------------------------------------------------------------------------------------------


# ---------------------------Creating instructions from points-----------------------------------
# painting_points = [[X,Y],[X,Y],...]
def create_manual_instructions(d, painting_points):
    """
    :param d: the length of the arms of roboto
    :param painting_points: [[X,Y],[X,Y],...] coordinates od the specific line to draw
    :return: alpha_vec, beta_vec: the anges vectors of the points to draw
    """
    alpha_vec = []
    beta_vec = []

    for point in painting_points:
        # claculate the angles (in degrees) of the current point
        calculator = Calculator.Calc(point[0], point[1], d)
        calculator.CalculateAlphaAndBeta()
        alpha = calculator.alpha
        beta = calculator.beta

        # append the set of angels only if they are valid
        if (np.isnan(alpha) or np.isnan(beta)):
            continue
        else:
            alpha_vec.append(alpha)
            beta_vec.append(beta)

    # alpha_vec, beta_vec = lpf.downsizing_data(alpha_vec, beta_vec)

    return alpha_vec, beta_vec
# ------------------------------------------------------------------------------------------------


# ------------------------- send instructions to De-Boto -----------------------------------------
def send_alpha_beta_vectors(d, alpha_vec, beta_vec, de_boto_comm):

    commands_vector = de_boto_comm.prepare_data_to_send(alpha_vec, beta_vec)

    de_boto_comm.SEND_With_TCP(commands_vector)
    import time
    time.sleep(len(alpha_vec))#time for testing until adding stop buttom
# ------------------------------------------------------------------------------------------------


# ------------------------The functions that runs it all -----------------------------------------
def activate_De_Boto(img_path):
    """
    this function will read the img from the specified location, convert it,
    and then send it to ROBOTO, so he can draw it :)

    :param img_path: a path to the desired img to draw
    :return: 
    """

    # parameters definitions
    d = 120

    # connect to De Boto
    tcp_send.debug = debug
    de_boto_comm = tcp_send.tcp_connection()
    

    # convert the img to a vector of lines to sketch
    lines = linedraw.sketch(img_path)
    # return list of polylines, eg.
    # [[(x,y),(x,y),(x,y)],[(x,y),(x,y),...],...]

    # converts the drawing area to be inside the feasible area
    lines = normalize_size_linedraw(lines, visualize = False)

    # for every line, convert the (x,y) locations to angles for roboto
    for vector in lines:
        alpha_vec, beta_vec = create_manual_instructions(d, vector)

        # send the commands to De-Boto
        if len(alpha_vec) != 0:
            send_alpha_beta_vectors(d, alpha_vec, beta_vec, de_boto_comm)

    print("all the img has been transferred to De-Boto, hope you like what you see :)")
    de_boto_comm.Move_to_start()
    exit(0)
# ------------------------------------------------------------------------------------------------



# --------------------------------RUN------------------------------------------

"""
    to actviate roboto,
     connect it (physically),
      enter the path and then run this file.
      
    example = 
    run_tests("./images/eiffel.jpg")

"""

# # linedraw'
if __name__ == '__main__':
    img_path = "./images/pinguin.jpg"
    activate_De_Boto(img_path)
    activate_De_Boto(img_path)
    activate_De_Boto(img_path)




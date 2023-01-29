from turtle import color
import numpy as np
import matplotlib.pyplot as plt

def show_lines_in_lut(lines, y_offset):
    x_lines = np.array([])
    y_lines = np.array([])
    for line in lines:
        for dot in line:     
            x_lines = np.append(x_lines,dot[0])
            y_lines = np.append(y_lines,dot[1])

    d = 120
    alpha =  np.zeros((180,180))
    beta = np.zeros((180,180))
    for i in range(alpha.shape[0]):
        alpha[i,:] = np.arange(0,180,1)
        beta[i,:] = np.arange(i,180+i,1)
    

    con_one = np.bitwise_and(beta <= alpha + 140, beta >= alpha)
    con_two = np.bitwise_and(alpha >= 0, alpha <= 180)
    con_three = np.bitwise_and(beta >= 0, beta <= 180)
    con_four = np.bitwise_and(con_one,con_two)
    all_con = np.bitwise_and(con_three,con_four)



    alpha_valid = alpha[all_con]*np.pi/180
    beta_valid = beta[all_con]*np.pi/180

    R = np.sqrt(2*d**2*(1+np.cos((beta_valid-alpha_valid))))
    X = R*np.cos((alpha_valid+beta_valid)/2)
    Y = R*np.sin((alpha_valid+beta_valid)/2)

    # # y_offset = how far to place De-Boto from the paper 
    # # Notic- we have a "built-in" offset betwenn the paper and the rotation axis (due to the base of ROBOTO (approx. 20mm))
    built_in_offset = 20 # CHANGE ONLY IF PHISICAL BUILD CHANGES
    y_offset = built_in_offset + 40
    plt.scatter(X,Y-y_offset)
    plt.plot([-148,148, 148, -148,-148], [0,0 ,210,210 ,0])

    y_mid =105 + y_offset

    # rectangle
    x_delta_rec = 120
    y_delta_rec = 45
    plt.plot([-x_delta_rec, x_delta_rec, x_delta_rec, -x_delta_rec, -x_delta_rec],
            [y_mid-y_delta_rec, y_mid - y_delta_rec, y_mid + y_delta_rec, y_mid + y_delta_rec, y_mid - y_delta_rec],
            color='red')


    #square
    delta_sqr = 65
    plt.plot([-delta_sqr, delta_sqr, delta_sqr, -delta_sqr, -delta_sqr], [y_mid - delta_sqr, y_mid - delta_sqr, y_mid + delta_sqr, y_mid + delta_sqr, y_mid - delta_sqr], color='black')
    plt.scatter(x_lines,y_lines)
    plt.show()

def find_image_bounderies(resolution):
    """
    :param resolution = [w,h] of image
    returns:
    area of drawing inside the paper
    spin if there is a need to spin the image
    """
    ratio_of_picture = resolution[0]/resolution[1]

    # y_offset = how far to place De-Boto from the paper 
    # Notic- we have a "built-in" offset betwenn the paper and the rotation axis (due to the base of ROBOTO (approx. 20mm))
    built_in_offset = 20 # CHANGE ONLY IF PHISICAL BUILD CHANGES
    y_offset = built_in_offset + 40

    x_mid = 0
    y_mid = 105 + y_offset
    #defult x 
    x_delta = 100  #120
    #defult y
    y_delta = 25 #45
    spin = False

    if(ratio_of_picture == 1): # if the picture is a square
        spin = False
        x_delta = 65
        y_delta = 65

    else:
        # if(ratio_of_picture > 1):# w >h
        spin = False
        if (ratio_of_picture <= x_delta/y_delta ):
            x_delta = y_delta*ratio_of_picture
            y_delta = y_delta

        elif (ratio_of_picture > x_delta/y_delta ):
            x_delta = x_delta
            y_delta = x_delta/ratio_of_picture
        # else: # h > w
        #     ratio_of_picture= 1/ratio_of_picture
        #     spin = True
        #     if (ratio_of_picture <= x_delta/y_delta ):
        #         x_delta = y_delta*ratio_of_picture
        #         y_delta = y_delta
        #
        #     elif (ratio_of_picture > x_delta/y_delta ):
        #         x_delta = x_delta
        #         y_delta = x_delta/ratio_of_picture
    drawing_area = [x_mid - x_delta, x_mid + x_delta], [y_mid - y_delta, y_mid + y_delta]
    return(drawing_area, spin, y_offset)
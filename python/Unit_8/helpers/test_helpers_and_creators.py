from enum import Flag
from operator import index
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

def change_size_of_img(src_dir, name):
    img = cv2.resize(cv2.imread(os.path.join(src_dir, name)), (297, 210), cv2.INTER_NEAREST)
    cv2.imwrite(os.path.join(src_dir, "small_" + name), img)


def create_simple_bw_circle():
    #there may be some really stupid shit, im tired, but a point of tryal to do stuff ... forgot the start, well, you get it
    img = np.zeros([297, 210, 3], dtype=np.uint8)
    img.fill(255)  # or img[:] = 255
    cv2.circle(img, (130, 150), 15, (0, 0, 0), thickness = 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    return im_bw


def create_simple_bw_line():
    #there may be some really stupid shit, im tired, but a point of tryal to do stuff ... forgot the start, well, you get it
    img = np.zeros([297, 210, 3], dtype=np.uint8)
    img.fill(255)  # or img[:] = 255
    cv2.line(img, (100, 100), (150,200), (0, 0, 0), thickness = 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    return im_bw


def create_middle_line__angles__():
    a_vec = np.arange(0, 55, 2)
    b_vec = 180 - a_vec
    return a_vec, b_vec




# FIXME - change names to better ones, all i came up with is dotted graph.....
def plot_graph(graph_dots, discription, y_range):
    plt.figure()       
    plt.plot(graph_dots,'-bo')
    plt.title(discription)
    plt.grid( axis = 'y')
    plt.yticks(np.arange(y_range[0], y_range[1]+1, 1.0))
    plt.show()


def show_img(img, title):
    plt.figure()
    plt.imshow(img)
    plt.colorbar()

    plt.title(title)

##TODO :FIX
def plot_in_real_time(commands_vector,d):
    alpha_vec = commands_vector[0::2]*np.pi/180
    beta_vec = commands_vector[1::2]*np.pi/180
    L = np.sqrt(2*pow(d,2)*(1+np.cos(beta_vec-alpha_vec)))
    benefactor_angles = (beta_vec+alpha_vec)/2
    X = L*np.cos(benefactor_angles)
    Y = L*np.sin(benefactor_angles)
    import turtle
    wn = turtle.Screen()
    t = turtle.Turtle()
    t.speed(0)
    t.pencolor('blue')
    t.goto(-148,0)
    t.pd()
    t.goto(148,0)
    t.goto(148,210)
    t.goto(-148,210)
    t.goto(-148,0)
    t.pencolor('white')
    t.goto(X[0],Y[0])
    t.pencolor('black')
    for i in range(1,X.shape[0]-1):
        t.goto(X[i],Y[i])
    


    


def close_all_plots():
    plt.close('all')


def show_all_plots():
    plt.show()


def pause_plots_for_seconeds(time):
    plt.pause(time)


def sort_by_Norm2(X,Y, alpha_vec = [], beta_vec = [] ):
    X_copy = np.copy(X)
    Y_copy = np.copy(Y)
    X_sorted = np.array([])
    Y_sorted = np.array([])
    if alpha_vec.shape[0] >0 :
        alpha_sorted = np.array([])
        beta_sorted = np.array([])
    min_index = np.array([],dtype=int)
    min_index = np.append(min_index , np.argmin(X_copy))
    X_sorted = np.append(X_sorted,X_copy[min_index[-1]])
    Y_sorted= np.append(Y_sorted,Y_copy[min_index[-1]])

    if alpha_vec.shape[0] >0 :
        alpha_sorted = np.append(alpha_sorted,alpha_vec[min_index[-1]])
        beta_sorted= np.append(beta_sorted,beta_vec[min_index[-1]])

    X_copy = np.delete(X_copy,min_index[-1])
    Y_copy = np.delete(Y_copy,min_index[-1])
    for i in range(1,X_copy.shape[0]):
        distance = (np.power(X_copy-X_sorted[-1],2) + np.power(Y_copy-Y_sorted[-1],2))
        min_index = np.append(min_index , np.argmin(distance))
        X_sorted = np.append(X_sorted,X_copy[min_index[-1]])
        Y_sorted= np.append(Y_sorted,Y_copy[min_index[-1]])
        if alpha_vec.shape[0] > 0 :
            alpha_sorted = np.append(alpha_sorted,alpha_vec[min_index[-1]])
            beta_sorted= np.append(beta_sorted,beta_vec[min_index[-1]])
        X_copy = np.delete(X_copy,min_index[-1])
        Y_copy = np.delete(Y_copy,min_index[-1])
    if alpha_vec.shape[0] >0 :
        return X_sorted, Y_sorted, alpha_sorted, beta_sorted 
    else:
         return X_sorted, Y_sorted


def angle_vectors_to_paper(commands_vector,d):
    alpha_vec = commands_vector[0::2]*np.pi/180
    beta_vec = commands_vector[1::2]*np.pi/180
    L = np.sqrt(2*pow(d,2)*(1+np.cos(beta_vec-alpha_vec)))
    benefactor_angles = (beta_vec+alpha_vec)/2
    X = L*np.cos(benefactor_angles)
    Y = L*np.sin(benefactor_angles)
    X_sorted, Y_sorted, alpha_sorted, beta_sorted  = sort_by_Norm2(X,Y, alpha_vec, beta_vec)
    #plotting in real time for debug
    plot_graph(X ,"X graph by index" , (np.min(X),np.max(X)))
    plot_graph(Y ,"Y graph by index" , (np.min(Y),np.max(Y)))
    plot_graph(X_sorted ,"X sorted graph by index" , (np.min(X),np.max(X)))
    plot_graph(Y_sorted ,"Y sorted graph by index" , (np.min(Y),np.max(Y)))
    plot_graph(alpha_sorted,"alpha graph by index" , (np.min(alpha_sorted),np.max(alpha_sorted)))
    plot_graph(beta_sorted ,"beta graph by index" , (np.min(beta_sorted),np.max(beta_sorted)))
    plt.figure("repesntation on paper")
    plt.xlim((-148,148))
    plt.ylim((0,210))
    plt.scatter(X,Y)
    plt.figure("repesntation on paper in real time")
    plt.xlim((-148,148))
    plt.ylim((0,210))
    for i in range(X_sorted.shape[0]):
        plt.scatter(X_sorted[i], Y_sorted[i])
        plt.pause(0.3)
    plt.show()
    ################################
    return alpha_sorted*180/np.pi, beta_sorted*180/np.pi


def find_drawing_area(bw_img):
    drawing_sqare = np.zeros(bw_img.shape())
    mid_point = np.floor(bw_img.shape/2)
    i = 0
    drawing_sqare[mid_point[0]-i : mid_point[0]+i,mid_point[1]-i : mid_point[1]+i] = 1
    flag = np.any(np.bitwise_and(drawing_sqare,bw_img))
    
    while(flag):
        drawing_sqare[mid_point[0]-i : mid_point[0]+i,mid_point[1]-i : mid_point[1]+i] = 1
        flag = np.any(np.bitwise_and(drawing_sqare,bw_img))

    i = i-1
    drawing_sqare = np.zeros(bw_img.shape())
    drawing_sqare[mid_point[0]-i : mid_point[0]+i,mid_point[1]-i : mid_point[1]+i] = 1
    return(drawing_sqare)


# change_size_of_img("./images/", "pinguin.jpg")
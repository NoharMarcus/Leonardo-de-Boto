from random import *
import turtle
from PIL import Image, ImageDraw, ImageOps
from lines.util import *


def sortlines(lines):
    print("optimizing stroke sequence...")
    clines = lines[:]
    slines = [clines.pop(0)]
    while clines != []:
        x,s,r = None,1000000,False
        for l in clines:
            d = distsum(l[0],slines[-1][-1])
            dr = distsum(l[-1],slines[-1][-1])
            if d < s:
                x,s,r = l[:],d,False
            if dr < s:
                x,s,r = l[:],s,True

        clines.remove(x)
        if r == True:
            x = x[::-1]
        slines.append(x)
    return slines

def visualize(lines):
    import turtle
    offset_x = 148
    offset_y = 105
    wn = turtle.Screen()
    wn.setup(width = 297,height = 500,starty=250)
    t = turtle.Turtle()
    t.speed(0)
    t.pencolor('blue')
    t.pu()
    t.goto(-offset_x,-offset_y)
    t.pd()
    t.goto(-offset_x,-offset_y)
    t.goto(offset_x,-offset_y)
    t.goto(offset_x,offset_y)
    t.goto(-offset_x,offset_y)
    t.goto(-offset_x,-offset_y)
    
    t.pencolor('red')
    for i in range(0,len(lines)):
        for p in lines[i]:
            t.goto(p[0],p[1]-offset_y)
            t.pencolor('black')
        t.pencolor('red')
    turtle.mainloop()

if __name__=="__main__":
    import linedraw
    linedraw.draw_hatch = False
    lines = linedraw.sketch("C:/Users/sharo/OneDrive - Technion/Leonardo_De_Boto/Leonardo De Boto/Leonardo-de-Boto/python/images/hi.png")
    #lines = sortlines(lines)
    visualize(lines)


def draw_lines(lines_with_hatch,line_without_hatch,root):
    from tkinter import Tk, LEFT
    from turtle import Canvas, RawTurtle, TurtleScreen
    offset_x = 148
    offset_y = 105
    # set up the environment
    canvas1 = Canvas(root, width=297, height=210)
    canvas2 = Canvas(root, width=297, height=210)
    canvas1.grid(column = 0 ,row = 0)
    canvas2.grid(column = 3 ,row = 0)

    s1 = TurtleScreen(canvas1)
    s2 = TurtleScreen(canvas2)

    t1 = RawTurtle(canvas1)
    t1.speed(0)
    t1.pencolor('red')
    t1.pd()

    t2 = RawTurtle(canvas2)
    t2.speed(0)
    t2.pencolor('red')
    t2.pd()

    for i in range(0,len(lines_with_hatch)):
        for p in lines_with_hatch[i]:
            t1.goto(p[0],(p[1]-offset_y))
            t1.pencolor('black')
        t1.pencolor('red')

    for i in range(0,len(line_without_hatch)):
        for p in line_without_hatch[i]:
            t2.goto(p[0],(p[1]-offset_y))
            t2.pencolor('black')
        t2.pencolor('red')

    return(s1 , s2)
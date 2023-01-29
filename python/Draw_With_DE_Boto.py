from distutils.cmd import Command
import tkinter as tk
from tkinter import CENTER, Frame, filedialog
from turtle import bgcolor, color
import turtle    
from PIL import Image, ImageTk
from lines import strokesort as strokesort
from  lines import linedraw as linedraw
from roboto_main import normalize_size_linedraw,activate_De_Boto
from turtle import TurtleScreen
from helpers import im_from_lines
import roboto_main

#constants
DE_boto_photo =".\images\Leonardo_De_Boto.png"




root = tk.Tk()

canvas = tk.Canvas(root,width = 100 , height = 100 ,bg = "#fceadc" )
canvas.grid(columnspan = 3)


#new window for hatch vs no hatch
def new_canvas(filename):
     #draw with hatch button
    draw_with_hatch_text = tk.StringVar()
    draw_with_hatch_button = tk.Button(root, textvariable = draw_with_hatch_text , command = lambda:send_drawing_to_function(filename,True)
                                        , font = "Raleway" ,bg ="#36aeb7" ,activebackground = "#36aeb7")
    draw_with_hatch_text.set("draw with hatch")
    draw_with_hatch_button.grid(column = 0, row = 1 )

    #draw without hatch button
    draw_without_hatch_text = tk.StringVar()
    draw_without_hatch_button = tk.Button(root, textvariable = draw_without_hatch_text , command = lambda:send_drawing_to_function(filename,False) 
                                            , font = "Raleway" ,bg ="#36aeb7" ,activebackground = "#36aeb7")
    draw_without_hatch_text.set("draw without hatch")
    draw_without_hatch_button.grid(column = 3, row = 1 )

    
    #draw using image
    linedraw.draw_hatch = True
    lines_with_hatch = normalize_size_linedraw(linedraw.sketch(filename),False)
    linedraw.draw_hatch = False
    line_without_hatch = normalize_size_linedraw(linedraw.sketch(filename),False)

    canvas.config(width = 0, height= 210,bg = "#fceadc")
    
    draw_with_hatch_img = ImageTk.PhotoImage(im_from_lines.create_img_from_lines(lines_with_hatch))
    draw_without_hatch_img = ImageTk.PhotoImage(im_from_lines.create_img_from_lines(line_without_hatch))


    

    label_with_hatch = tk.Label(image=draw_with_hatch_img)
    label_without_hatch = tk.Label(image=draw_without_hatch_img)

    label_with_hatch.image = draw_with_hatch_img
    label_without_hatch.image = draw_without_hatch_img

    label_with_hatch.grid(column = 0 ,row = 0)
    label_without_hatch.grid(column = 3, row = 0)
    
#drawing options
def send_drawing_to_function(filename,draw_with_hatch):
    sending_text = tk.Label(root, text = "Drawing...",font = "Raleway" , bg= "#fceadc")
    sending_text.grid(column = 1 ,row = 1)
    linedraw.draw_hatch = draw_with_hatch
    roboto_main.activate_De_Boto(filename)

    root.destroy()
    root2 = tk.Tk()
    canvas = tk.Canvas(root2,width = 300 , height = 300 ,bg = "#fceadc" )
    instruction = tk.Label(root2, text = "Drawing...",font = "Raleway" , bg= "#fceadc")
    instruction.place(relx=0.5, rely=0.5, anchor=CENTER)
    root2.mainloop()

#browsing for image function
def open_image():
    logo_label.destroy()
    browse_button.destroy()
    instruction.destroy()
    f_types = [('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = Image.open(filename)
    new_canvas(filename)

##instructions
instruction = tk.Label(root, text = "Select a picture from your computer",font = "Raleway" , bg= "#fceadc")
instruction.grid(columnspan = 3,column = 0 ,row = 1)
   

#browse button
browse_text =  tk.StringVar()
browse_button = tk.Button(root, textvariable = browse_text , command= lambda:open_image() , font = "Raleway" ,bg ="#36aeb7" ,activebackground = "#36aeb7")
browse_text.set("Browse")
browse_button.grid(column = 1, row = 2 )


#logo
logo = Image.open(DE_boto_photo)
logow , logoh = logo.size

logo = logo.resize((int(logow/3),int(logoh/3)))
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image = logo)
logo_label.image = logo
logo_label.grid(column = 1, row = 0)


root.mainloop()
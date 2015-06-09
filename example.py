#!/usr/bin/env python3
# tkinter-png - example of using tkinter and pypng to display pngs (albeit reduced quality)
# in nothing but pure python. Can use RGBA images, but alpha is opaque or transparent only.
# v0.7 - Example code and module seperated out

from tkinter import *
from tkinter_png import *

## MAIN ##

# Setup window
root = Tk()
root.title("Loaded image")

# Setup our PngImageTk objects
photo1 = PngImageTk("trans.png")
photo2 = PngImageTk("transbg.png")
        
# Create canvas object
c = Canvas(root, width=photo1.w, height=photo1.h)
c.pack()

# Convert and place on canvas
photo1.convert()
photo2.convert()
bg = c.create_image(0, 0, image=photo2.image, anchor=NW)
box = c.create_rectangle(1,1,21,21, fill="red")
text = c.create_image(0, 0, image=photo1.image, anchor=NW) #place our photoimage onto canvas in NW

# moving box to demonstrate transparency
bx = 0
by = 0
xmove = 0
ymove = 0
def moveBox(bx, by, xmove, ymove):
        if bx +20 > photo1.w:
                xmove = -1
        elif bx < 1:
                xmove = 1
        if by + 20 > photo1.h:
                ymove = -2
        elif by < 1:
                ymove = 2
        c.move(box, xmove, ymove)
        c.update()
        bx += xmove
        by += ymove
        root.after(10, moveBox, bx, by, xmove, ymove)

root.after(10, moveBox, bx, by, xmove, ymove)
root.mainloop()

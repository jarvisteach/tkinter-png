#!/usr/bin/env python3
# tkpng - example of using tkinter and pypng to display pngs (albeit reduced quality)
# in nothing but pure python. Can use RGBA images, but the alpha is stripped.
# v0.2 - image.put() places entire rows of pixels at a time rather than one by one (about 2x as fast!)

from array import *
from tkinter import *
import png

# Used to split each row into pairs of RGB or RGBA values
def chunks(l, n):
        return [l[i:i+n] for i in range(0, len(l), n)]

# Read image, create list of pixel RGBA values
r = png.Reader("image.png")
w, h, pixels, meta = r.asRGBA8() #forcing alpha needed to avoid exceptions, no major speed loss vs RGB-only
pixeldata = list(pixels) #pixeldata has each row of the image as an array

# Setup window, canvas and image
root = Tk()
root.title("Loaded image.png")
c = Canvas(root, width=w, height=h)
c.pack()
image = PhotoImage(width=w, height=h) #use photoimage as temporary oject to write to canvas

x = 0
y = 0

for row in pixeldata:
        row = row.tolist() #convert from array to list
        chunked = chunks(row, 4) #RGBA format, so 4 values
        rowline = "{"
        
        for item in chunked:
                del item[-1] #tkinter can't handle alpha values, so remove them
                RGB = "#%02x%02x%02x" % tuple(item) #convert to 8-bit RGB hex format
                #image.put(RGB,(x,y)) #place single pixels into a photoimage
                rowline += RGB + " "
                
                x += 1
                if x == w:
                        y += 1
                        x = 0
                        
        rowline += "}"
        image.put(rowline,(0,y))


c.create_image(0, 0, image=image, anchor=NW) #place our photoimage onto canvas in NW
root.mainloop()

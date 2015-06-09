#!/usr/bin/env python3
# tkpng - example of using tkinter and pypng to display pngs (albeit reduced quality)
# in nothing but pure python. Can use RGBA images, but the alpha is stripped.
# This may be short but it took a long time!! >.<
# v0.1 - uses image.put() to place each individual pixel instead of one-pixel rectangles

from array import *
from tkinter import *
import png

# Used to split each row into pairs of RGB or RGBA values
def chunks(l, n):
	return [l[i:i+n] for i in range(0, len(l), n)]

# Read image, create list of pixel RGBA values
r = png.Reader("image.png")
w, h, pixels, meta = r.asRGBA() #forcing alpha needed to avoid exceptions, no major speed loss vs RGB-only
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
	
	for item in chunked:
		del item[-1] #tkinter can't handle alpha values, so remove them
		RGB = "#%02x%02x%02x" % tuple(item) #convert to 8-bit RGB hex format
		#c.create_rectangle(x, y, x+1, y+1, fill=RGB, outline=RGB) #draw 1 pixel rect
		image.put(RGB,(x,y)) #place single pixels into a photoimage
		
		x += 1
		
		if x == w:
			y += 1
			x = 0

c.create_image(0, 0, image=image, anchor=NW) #place our photoimage onto canvas in NW
root.mainloop()

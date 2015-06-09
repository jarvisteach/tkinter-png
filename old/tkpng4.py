#!/usr/bin/env python3
# tkpng - example of using tkinter and pypng to display pngs (albeit reduced quality)
# in nothing but pure python. Can use RGBA images, but the alpha is stripped.
# v0.4 - optimised to use single .put() instead of row by row

from array import *
from tkinter import *
import png

class PngImageTk(object):
        """A png image loaded and placed into a tkinter.PhotoImage object"""
        def __init__(self, filename):
                # Read image, create list of pixel RGB or RGBA values
                r = png.Reader(filename)
                # Try to use RGB8 load if no alpha chanel otherwise use alpha (RGBA8)
                try:
                        self.w, self.h, self.pixels, self.meta = r.asRGB8()
                except:
                        self.w, self.h, self.pixels, self.meta = r.asRGBA8()
                self.pixeldata = list(self.pixels) #pixeldata has each row of the image as an array
                self.x = 0
                self.y = 0
                self.image = PhotoImage(width=self.w, height=self.h) #use photoimage as temporary oject to write to canvas

        # Print meta data for image
        def __str__(self):
                rep = "Width:", self.width, "\n"
                rep += "Height:", self.height, "\n"
                rep += "Bitdepth:", self.meta["bitdepth"], "\n"
                rep += "Greyscale:", self.meta["greyscale"], "\n"
                rep += "Alpha:", self.meta["alpha"], "\n"
                return rep
        
        # Used to split each row into pairs of RGB or RGBA values
        def chunks(self, l, n):
                return [l[i:i+n] for i in range(0, len(l), n)]

        # Convert pixeldata into a PhotoImage object
        def  convert(self):
                if self.meta["alpha"] == True:
                        values = 4
                else:
                        values = 3
                i = 0
                pixelrows = []
                for row in self.pixeldata:
                        row = row.tolist() #convert from array to list
                        chunked = self.chunks(row, values) #RGB/RGBA format = 3/4 values
                        rowline = []
                        
                        for item in chunked:
                                if self.meta["alpha"] == True:
                                        del item[-1] #tkinter can't handle alpha values, so remove them
                                RGB = "#%02x%02x%02x" % tuple(item) #convert to 8-bit RGB hex format
                                rowline.append(RGB)
                                #print(RGB)
                                #print(rowline)

                        pixelrows.append(rowline)      

                pixelrows = tuple(tuple(x) for x in pixelrows)
                self.image.put(pixelrows,(0,0, 550,400))
                #self.image.write("debug.gif", format="gif")

# MAIN

# Setup window
root = Tk()
root.title("Loaded image.png")

# Setup our PngImageTk object
photo1 = PngImageTk("image.png")
# Create canvas object
c = Canvas(root, width=photo1.w, height=photo1.h)
c.pack()
# Convert and place on canvas
photo1.convert()
c.create_image(0, 0, image=photo1.image, anchor=NW) #place our photoimage onto canvas in NW

root.mainloop()

#!/usr/bin/env python3
# tkinter-png - example of using tkinter and pypng to display pngs (albeit reduced quality)
# in nothing but pure python. Can use RGBA images, but alpha is opaque or transparent only.
# v0.6 - Better demonstrates image transparency by using a moving box underneath the text

from array import *
from tkinter import *
import png


## tkinter hacking section ##

# Define our new tkinter.PhotoImage functions and override the stock version
class PhotoImage(PhotoImage):
	def transGet(self, x, y):
		"""Returns a boolean if pixel at (x,y) is transparent"""
		return self.tk.call(self.name, "transparency", "get", x, y)
	
	def transSet(self, x, y, alpha):
		"""Makes the pixel at (x,y) transparent if alpha is is true or opaque otherwise"""
		self.tk.call(self.name, "transparency", "set", x, y, alpha)
	
	# tkinter already has a gimped version of copy, but it's pretty useless
	# this version is still lacking and doesn't have all options, but is actually usable
	def copy(self, sourceImage, fromBox=None, toBox=None):
		"""Copies from region of sourceImage at fromBox to current image at toBox"""
		args = (self.name, "copy", sourceImage)
		if fromBox:
			if fromBox[0] == "-from":
				fromBox = fromBox[1:]
			args = args + ("-from",) + tuple(fromBox)
		if toBox:
			if toBox[0] == "-to":
				toBox = toBox[1:]
			args = args + ("-to",) + tuple(toBox)
		self.tk.call(args)
	
	def redither(self):
		"""Recalculate dithering used in PhotoImages to fix errors that may occur if image data was supplied in chunks"""
		self.tk.call(self.name, "redither")
	
	def data(self, bg=None, fromBox=None, grey=None):
		"""Returns image data in the form of a string"""
		args = (self.name, "data")
		if bg:
			if bg[0] == "-background":
				bg = bg[1:]
			args = args + ("-background",) + tuple(bg)
		if fromBox:
			if fromBox[0] == "-from":
				fromBox = fromBox[1:]
			args = args + ("-from",) + tuple(fromBox)
		if grey:
			if grey == True or grey == "-grayscale":
				args = args + ("-grayscale",)


## PngImageTk section ##

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
		
		pixelrows = []
		alphapixels = []
		
		for row in self.pixeldata:
			row = row.tolist() #convert from array to list
			chunked = self.chunks(row, values) #RGB/RGBA format = 3/4 values
			rowline = []
						
			for item in chunked:
				if self.meta["alpha"] == True:
					# if 100% transparent, remember this pixel so we can make it transparent later
					if item[3] == 0:
						alphapixels.append((self.x, self.y))
					del item[-1] #remove alpha bit
				
				RGB = "#%02x%02x%02x" % tuple(item) #convert to 8-bit RGB hex format
				rowline.append(RGB)
				
				# Increment position, used for tracking coordinates of transparent pixels
				self.x += 1
				if self.x == self.w:
					self.y += 1
					self.x = 0

			pixelrows.append(rowline)      

		pixelrows = tuple(tuple(x) for x in pixelrows) #convert our list of lists into a tuple of tuples
		self.image.put(pixelrows,(0,0, 550,400)) #pixels are finally written to the PhotoImage
		
		# If we have alphapixels, set each stored coordinate to transparent
		if alphapixels:
			for item in alphapixels:
				self.image.transSet(item[0],item[1], "True")


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

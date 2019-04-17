import numpy as np 
from sys import exit

class Editor() :
	# image data structure
	image = np.matrix(0)
	# variable to keep track of image intialisation
	initialised = False

	# check row and column indices are in bounds
	def inBounds(self, row, col) :
		if (row > self.image.shape[0] - 1) :
			return False
		if (row < 0) :
			return False
		if (col > self.image.shape[1] - 1) :
			return False
		if (col < 0) :
			return False
		return True

	# set pixel color
	def setColor(self, row, col, color) :
		if (self.inBounds(row, col)) :
			self.image[row][col] = color

	# get pixel color
	def getColor(self, row, col) :
		if (self.inBounds(row,col)) :
			return self.image[row][col]
		return ord('0')

	# clear the image
	def clear(self, cmd) :
		# check image is initialised and throw error if it isn't
		if (self.initialised) :
			self.image.fill(ord('0'))
		else :
			print("Error: image not initialised.")

	# set color of a defined pixel
	def color(self, cmd) :
		# check image is initialised and throw error if it isn't
		if (self.initialised) :
			col = int(cmd[2]) - 1 
			row = int(cmd[4]) - 1
			color = ord(cmd[6])
			self.setColor(row, col, color)
		else :
			print("Error: image not initialised.")

	# intialise the image
	def create(self, cmd) :
		M = int(cmd[2])
		N = int(cmd[4])
		self.image = np.zeros((N,M))
		self.image.fill(ord('0'))
		self.initialised = True

	# print out the image
	def show(self, cmd) :
		# check image is initialised and throw error if it isn't
		if (self.initialised) :
			rows = self.image.shape[0]
			cols = self.image.shape[1]

			for i in range(0, rows):
				for j in range(0, cols):
					print(chr(int(self.image[i, j])), end='')
				print("")
		else :
			print("Error: image not initialised.")

	# terminate program
	def end(self, cmd) :
		exit()

	# fill the defined vertical region
	def vertical(self, cmd) :
		# check image is initialised and throw error if it isn't
		if (self.initialised) :
			col = int(cmd[2]) - 1
			row1 = int(cmd[4]) - 1 
			row2 = int(cmd[6])
			color = ord(cmd[8])

			for i in range(row1, row2) :
				self.setColor(i, col, color)
		else :
			print("Error: image not initialised.")

	# fill the defined horizontal region
	def horizontal(self, cmd) :
		# check image is initialised and throw error if it isn't
		if (self.initialised) :
			col1 = int(cmd[2]) - 1
			col2 = int(cmd[4])
			row = int(cmd[6]) - 1
			color = ord(cmd[8])

			for i in range(col1, col2) :
				self.setColor(row, i, color)
		else :
			print("Error: image not initialised.")

	# fill region
	def fillRegion(self, row, col, color, start_color) :
		# check the current pixel is part of the region
		current_color = self.getColor(row, col)
		if (current_color == start_color) :
			# set new color for current pixel
			self.setColor(row, col, color)

			# fill connected pixels
			if (self.inBounds(row + 1, col)) :
				self.fillRegion(row + 1, col, color, start_color)
			if (self.inBounds(row - 1, col)) :
				self.fillRegion(row - 1, col, color, start_color)
			if (self.inBounds(row, col + 1)) :
				self.fillRegion(row, col + 1, color, start_color)
			if (self.inBounds(row, col - 1)) :
				self.fillRegion(row, col - 1, color, start_color)

	# prepare region filling
	def fill(self, cmd) :
		# check image is initialised and throw error if it isn't
		if (self.initialised) :
			# intialise region filling parameters
			col = int(cmd[2]) -1
			row = int(cmd[4]) - 1
			color = ord(cmd[6])
			start_color = self.getColor(row, col)
			# start region filling
			self.fillRegion(row, col, color, start_color)
		else :
			print("Error: image not initialised.")

	# dictionary of possible commands
	commands = {
		'I' : create,
		'C' : clear,
		'L' : color,
		'V' : vertical,
		'H' : horizontal,
		'F' : fill,
		'S' : show,
		'X' : end
	}

	# process one command
	def process(self, cmd) :
		self.commands[cmd[0]](self, cmd)

# intialise an image editor
editor = Editor()

# loop indefinitely while processing commands
while (1) :
	cmd = input("Next command: ")
	editor.process(cmd)
#!/usr/bin/python

from Tkinter import *
import random

# direction settings
UP          = 0
DOWN        = 1
LEFT        = 2
RIGHT       = 3

# timing settings
DELAY       = 200

# canvas settings
MIN_X       = 0
MIN_Y       = 0
MAX_X       = 640
MAX_Y       = 480
BLOCK_SIZE  = 5

def DEBUG(message):
    print message

class PySnakeApp(Frame):   
    # PySnakApp class initialization
    def __init__(self, parent):
        self.frame = Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.pack()

    # initialize UI objects
    def initUI(self):
        # setup application window
        self.parent.title("pySnake")
        self.pack(fill=BOTH, expand=1)
        # setup canvas to draw
        self.canvas = Canvas(self, background="black")
        self.canvas.pack(fill=BOTH, expand=True)
        # initialize snake
        self.snake = Snake(self.canvas)
	self.snake.addBlock()
	self.snake.addBlock()
	self.snake.addBlock()
	self.snake.addBlock()
        # bind keys
        self.parent.bind('<Up>', self.moveUp)
        self.parent.bind('<Down>', self.moveDown)
        self.parent.bind('<Left>', self.moveLeft)
        self.parent.bind('<Right>', self.moveRight)
        # run application
        self.runApp()

#        # initialize blocks
#        self.numBlocks = 5
#        self.blockList = []
#        self.drawBlocks()

#    # draw individual blocks in the main area
#    def drawBlocks(self):
#        minX = 10
#        minY = 10
#        maxX = self.x - 10
#        maxY = self.y - 10        
#        # populate empty block list
#        if (len(self.blockList) != self.numBlocks):
#            while (len(self.blockList) < self.numBlocks):
#                x = random.randint(minX, maxX)
#                y = random.randint(minY, maxY)
#                self.blockList.append(Block(self.canvas, x, y, "white"))

    # run application
    def runApp(self):
#        self.snake.addBlock()
        self.snake.moveSnake()
        if (self.snake.collisionDetected()):
            return
        self.canvas.after(DELAY, self.runApp)

    # key bindings
    def moveUp(self, event):
        self.snake.setDirection(UP)
    def moveDown(self, event):
        self.snake.setDirection(DOWN)
    def moveLeft(self, event):
        self.snake.setDirection(LEFT)
    def moveRight(self, event):
        self.snake.setDirection(RIGHT)

class Snake:
    def __init__(self, canvas):
        initX = 20
        initY = (MAX_Y - MIN_Y) / 2
        self.canvas = canvas
        self.head = Block(canvas, initX, initY, "red")
        self.head.setDirection(RIGHT)

    # add block to tail of snake
    def addBlock(self):
	tail = self.head
	while (tail.getNextBlock() != None):
    	    tail = tail.getNextBlock()
	newBlock = Block(self.canvas, tail.getX(), tail.getY(), "red")
	tail.setNextBlock(newBlock)

    # move each block in snake
    def moveSnake(self):
	# chase head by shifting to prior blocks position
	b = self.head
	x = b.getX()
        y = b.getY()
	while (b.getNextBlock() != None):
            n = b.getNextBlock()
            tmpX = n.getX()
	    tmpY = n.getY()
            n.setCoordinates(x, y)
            x = tmpX
            y = tmpY
	    b = n	    
	# move head in stored direction
	self.head.moveBlock()

    # check for collisions
    def collisionDetected(self):
        # self collision
        block = self.head
        while (block.getNextBlock() != None):
	    block = block.getNextBlock()
            if (block == self.head):       
		return True
        # wall collision
        if (self.head.getX() == MIN_X or
            self.head.getX() == MAX_X or
            self.head.getY() == MIN_Y or
            self.head.getY() == MAX_Y):
            return True
        # no collision
        return False

    # only set the head block direction
    def setDirection(self, direction):
        self.head.setDirection(direction)

class Block:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.direction = -1
        self.nextBlock = None
        # x,y coordinates for block center
        self.x = x
        self.y = y
        self.id = self.canvas.create_rectangle(x-5,y-5,x+5,y+5,fill=color)

    def getX(self):
        return self.x

    def getY(self): 
        return self.y

    # overload eq function to detect if two blocks have collided
    def __eq__(self, other):    
        return (abs(self.x - other.x) <= 5 and abs(self.y - other.y) <= 5)

    # set the block's direction of travel
    def setDirection(self, direction):
        self.direction = direction

    # return the block's direction of travel
    def getDirection(self):
        return self.direction

    # set linked block
    def setNextBlock(self, block):
        self.nextBlock = block

    # return linked block
    def getNextBlock(self):
        return self.nextBlock
    
    # move block to the set coordinates
    def setCoordinates(self, x, y):
        # x,y coordinates for block center
        self.x = x
        self.y = y
        self.canvas.coords(self.id,x-5,y-5,x+5,y+5)

    # move the block in the appropriate direction
    def moveBlock(self):
	d = self.direction
        shiftX = 0
        shiftY = 0
	if (d == UP):
	    shiftY -= 10
	elif (d == DOWN):
	    shiftY += 10
        elif (d == LEFT):
            shiftX -= 10
        elif (d == RIGHT):
            shiftX += 10
	self.x += shiftX
	self.y += shiftY
	self.setCoordinates(self.x, self.y)        
	#self.canvas.move(self.id, shiftX, shiftY)

def main():
    root = Tk()
    root.geometry("640x480+300+300")
    app = PySnakeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

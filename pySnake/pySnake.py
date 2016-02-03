#!/usr/bin/python
from Tkinter import *
import random

# pySnake is a simple version of the classic snake game
# missing functionality:
# - show score
# - 'you lose' message
# - randomly generated blocks don't check if space occupied by snake or existing block

# direction settings
UP          = 0
DOWN        = 1
LEFT        = 2
RIGHT       = 3

# timing settings
INIT_DELAY  = 100 # increase delay to 'build up' speed
MIN_DELAY   = 100
SPEED_UP    = 5

# canvas settings
MIN_X       = 0
MIN_Y       = 0
MAX_X       = 640
MAX_Y       = 480
MARGIN      = 15
BLOCK_SIZE  = 5
NUM_BLOCKS  = 5

# debug functionality prints string in terminal while application runs
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
        # setup canvas to draw objects
        self.canvas = Canvas(self, background="black")
        self.canvas.pack(fill=BOTH, expand=True)
        # initialize snake
        self.snake = Snake(self.canvas)
	    # initialize bites
        self.bites = Bites(self.canvas)
        # bind key events to key bindings
        self.parent.bind('<Up>', self.moveUp)
        self.parent.bind('<Down>', self.moveDown)
        self.parent.bind('<Left>', self.moveLeft)
        self.parent.bind('<Right>', self.moveRight)
        # run application
        self.delay = INIT_DELAY
        self.score = 0
        self.runApp()

    # run pySnake application
    def runApp(self):
	    # move snake
        self.snake.moveSnake()
	    # check if bite eaten by snake head
        if (self.bites.gotBite(self.snake.getHead())):
            # speed up, add score, grow snake
            if (self.delay > MIN_DELAY): self.delay -= SPEED_UP
            self.score += 10
            self.snake.growSnake()
        # check for collisions (end game)        
        elif (self.snake.collisionDetected()):
            endText = "YOU LOSE\nSCORE: {}".format(self.score)
            txt = self.canvas.create_text(MAX_X/2, MAX_Y/2)
            self.canvas.itemconfig(txt, font=("Verdana", 20, "bold"))
            self.canvas.itemconfig(txt, fill="red")
            self.canvas.itemconfig(txt, text=endText)
            return
        # time interval to runApp()
        self.canvas.after(self.delay, self.runApp)

    # key event bindings used to control snake movement
    def moveUp(self, event):
        self.snake.moveUp()
    def moveDown(self, event):
        self.snake.moveDown()
    def moveLeft(self, event):
        self.snake.moveLeft()
    def moveRight(self, event):
        self.snake.moveRight()

# class defining snake functionality
# snake is created using linked list of blocks
class Snake:
    def __init__(self, canvas):
        initX = 20
        initY = (MAX_Y - MIN_Y) / 2
        self.canvas = canvas
        self.direction = RIGHT
        self.head = Block(canvas, initX, initY, "red")		

    # return the head block
    def getHead(self):
        return self.head

    # add block to tail of snake
    def growSnake(self):
        tail = self.head
        while (tail.getNextBlock() != None):
            tail = tail.getNextBlock()
        newBlock = Block(self.canvas, tail.getX(), tail.getY(), "red4")
        tail.setNextBlock(newBlock)

    # functions controlling snake movement
    def moveUp(self):
        if (self.direction != DOWN):
            self.direction = UP
    def moveDown(self):
        if (self.direction != UP):
            self.direction = DOWN
    def moveLeft(self):
        if (self.direction != RIGHT):
            self.direction = LEFT
    def moveRight(self):
        if (self.direction != LEFT):
            self.direction = RIGHT

    # move snake
    def moveSnake(self):
		# move each block takes position of previous block
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
		x = self.head.getX()
		y = self.head.getY()
		if (self.direction == UP):		y -= BLOCK_SIZE*2
		elif (self.direction == DOWN):	y += BLOCK_SIZE*2
		elif (self.direction == LEFT):	x -= BLOCK_SIZE*2
		elif (self.direction == RIGHT): x += BLOCK_SIZE*2
		self.head.setCoordinates(x, y)

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

# class defining bites on map for snake to eat
class Bites:
    def __init__(self, canvas):
	self.canvas = canvas
	self.bites = []
	for n in range(0, NUM_BLOCKS):
	    self.addBite()

    # add random bite to list
    def addBite(self):
        minX = MIN_X + MARGIN
        maxX = MAX_X - MARGIN
        minY = MIN_Y + MARGIN
        maxY = MAX_Y - MARGIN
        # require generated point to be multiple of (BLOCK_SIZE * 2)
        # ensures that block will be align with path of snake movement
        x = 1
        y = 1
        while (x % 10 != 0): x = random.randint(minX, maxX)
        while (y % 10 != 0): y = random.randint(minY, maxY)
        self.bites.append(Block(self.canvas, x, y, "white"))

    # check for collition with snake head
    def gotBite(self, head):
        detected = False
        # return list containing collisions and remove from canvas
        removeBites = [x for x in self.bites if x == head]
        for b in removeBites:
            b.removeBlock()
            self.addBite()
            detected = True
        # remove block objects from current bite list
        self.bites[:] = [x for x in self.bites if not x == head]
        return detected
	
# class defining blocks used to create snake and bites
class Block:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        # allow blocks to form linked list to create snake
        self.nextBlock = None
        # block attributes
        self.x = x
        self.y = y
        size = BLOCK_SIZE
        self.id = self.canvas.create_rectangle(x-size,y-size,x+size,y+size,fill=color)

	# return block's current x coordinate
    def getX(self):
        return self.x

	# return block's current y coordinate
    def getY(self): 
        return self.y

    # overload eq function to detect if two blocks have collided
    def __eq__(self, other):
        size = BLOCK_SIZE
        return (abs(self.x - other.x) <= size and abs(self.y - other.y) <= size)

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
        size = BLOCK_SIZE
        self.canvas.coords(self.id,x-size,y-size,x+size,y+size)

    def removeBlock(self):
		self.canvas.delete(self.id)

def main():
    # create fixed size window and launch application
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    root.geometry('{}x{}'.format(MAX_X, MAX_Y))
    app = PySnakeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()


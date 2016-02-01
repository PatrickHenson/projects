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
        self.head.setDirection(3)

    # iterate through each linked block, move, and set the next direction
    def moveSnake(self):
        self.head.moveBlock()
        node = self.head
        while (node.getNextBlock() != None):
            direction = node.getDirection()
            node = node.getNextBlock()
            node.moveBlock()
            node.setDirection(direction)

    # check for collisions
    def collisionDetected(self):
        # self collision
        block = self.head
        while (block.getNextBlock() != None):
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
        self.id = self.canvas.create_rectangle(x-5, y-5, x+5, y+5, fill=color)

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

    # move the block in the appropriate direction
    def moveBlock(self):
        xDirection = 0
        yDirection = 0
        if (self.direction == UP):
            yDirection = -10
        elif (self.direction == DOWN):
            yDirection = 10
        elif (self.direction == LEFT):
            xDirection = -10
        elif (self.direction == RIGHT):
            xDirection = 10
        self.x += xDirection
        self.y += yDirection
        self.canvas.move(self.id, xDirection, yDirection)

def main():
    root = Tk()
    root.geometry("640x480+300+300")
    app = PySnakeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

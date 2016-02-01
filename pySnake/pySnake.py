#!/usr/bin/python

from Tkinter import *
import random

# value associated with each direction
up      = 0
down    = 1
left    = 2
right   = 3

class PySnakeApp(Frame):   
    # PySnakApp class initialization
    def __init__(self, parent):
        self.frame = Frame.__init__(self, parent)
        self.parent = parent
        self.x = 640
        self.y = 480
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
        self.snake = Snake(self.canvas, 20, self.y/2)
        self.snake.moveSnake()
        # initialize blocks
        self.numBlocks = 5
        self.blockList = []
        self.drawBlocks()
        # bind keys
        self.parent.bind('<Up>', self.moveUp)
        self.parent.bind('<Down>', self.moveDown)
        self.parent.bind('<Left>', self.moveLeft)
        self.parent.bind('<Right>', self.moveRight)

    # draw individual blocks in the main area
    def drawBlocks(self):
        minX = 10
        minY = 10
        maxX = self.x - 10
        maxY = self.y - 10        
        # populate empty block list
        if (len(self.blockList) != self.numBlocks):
            while (len(self.blockList) < self.numBlocks):
                x = random.randint(minX, maxX)
                y = random.randint(minY, maxY)
                self.blockList.append(Block(self.canvas, x, y, "white"))

    def moveUp(self, event):
        self.snake.setDirection(up)
    def moveDown(self, event):
        self.snake.setDirection(down)
    def moveLeft(self, event):
        self.snake.setDirection(left)
    def moveRight(self, event):
        self.snake.setDirection(right)

class Snake:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.head = Block(canvas, x, y, "red")
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
        self.canvas.after(100, self.moveSnake)

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

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    # function to detect if two blocks have collided
    def collision(self, other):    
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
        if (self.direction == up):
            yDirection = -10
        elif (self.direction == down):
            yDirection = 10
        elif (self.direction == left):
            xDirection = -10
        elif (self.direction == right):
            xDirection = 10
        self.canvas.move(self.id, xDirection, yDirection)

def main():
    root = Tk()
    root.geometry("640x480+300+300")
    app = PySnakeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

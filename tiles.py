#This store information about tiles
from turtle import Turtle
from players import *

class Tiles:
    def __init__(self, x, y,cellsize, color,tileValue):
        self.x = x
        self.y = y
        self.cellsize = cellsize
        self.color = color
        self.tileValue = tileValue
    
    def draw(self,turtle):
        tile = turtle
        tile.speed(0)
        tile.penup()
        tile.goto(self.x, self.y)
        tile.pendown()
        tile.fillcolor(self.color)
        tile.begin_fill()
        for i in range(0,4):
            tile.forward(self.cellsize)
            tile.right(90)
        tile.end_fill()
        tile.penup()
        tile.goto(self.x + self.cellsize / 2, self.y - self.cellsize)
        tile.pendown()
        tile.write(self.tileValue, align="center", font=("Poppins", 15, "normal"))
        tile.hideturtle()

    def getTileValue(self):
        return self.tileValue



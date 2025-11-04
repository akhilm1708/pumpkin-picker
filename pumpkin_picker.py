import turtle
import os
import random

wn = turtle.Screen()
wn.setup(width=1000, height=600)
wn.title("Pumpkin Picker")
wn.bgcolor("black")

#Cite: https://stackoverflow.com/questions/62613041/what-does-turtle-tracer-do
wn.tracer(0)

painter = turtle.Turtle()

class Pumpkin:
    """Class to represent and draw a pumpkin."""
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw_stem(self):
        """Draws the pumpkin given its attributes."""
        painter.goto(self.x, self.y)
        painter.pendown()
        painter.color(self.color)
        painter.begin_fill()
        painter.circle(self.radius)
        painter.end_fill()
        painter.penup()


class Stem:
    """Class to represent and draw a pumpkin stem."""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        """Draws the stem given its attributes."""
        painter.goto(self.x - self.width / 2, self.y)
        painter.pendown()
        painter.color("brown")
        painter.begin_fill()

        for _ in range(2):
            painter.forward(self.width)
            painter.left(90)
            painter.forward(self.height)
            painter.left(90)

        painter.end_fill()
        painter.penup()
 


pumpkin_colors = ["orange", "darkorange"]

# Draw multiple pumpkins (iteration):
for n in range(5):
    # Pumpkin parameters
    x = (n - 2) * 200
    y = 0
    size = 50
    color = random.choice(pumpkin_colors)

    # Draw pumpkin
    pumpkin = Pumpkin(x, y, size, color)
    pumpkin.draw_body()
    pumpkin.draw_stem()

#Cite: https://stackoverflow.com/questions/62613041/what-does-turtle-tracer-do
wn.update()

wn.mainloop()


from cmu_graphics import *

# blackhole class
class BlackHole:
    def __init__(self, x, y, size=20):
        self.x = x
        self.y = y
        self.size = size

    def draw(self):
        drawCircle(self.x, self.y, self.size, fill = 'black')

# bullet class
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.speed = -10  # Speed of the bullet

    def move(self):
        self.y += self.speed

    def draw(self):
        drawCircle(self.x, self.y, self.radius, fill='red')
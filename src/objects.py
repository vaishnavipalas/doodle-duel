from cmu_graphics import *
import math
from settings import *
import random


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

# monster class
class Monster:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 70
        self.image = Images.monsterImage

        # Citation: used ChatGPT to write the code to make monsters appear as if they are shaking
        self.baseX = x
        self.shakeAmplitude = 10
        self.shakeSpeed = 0.1
        self.shakeOffset = random.uniform(0, math.pi * 2)

    def move(self):
        # Refer to citation above
        self.x = self.baseX + self.shakeAmplitude * math.sin(self.shakeSpeed * app.time + self.shakeOffset)

    def draw(self):
        drawImage(self.image, self.x, self.y, width=self.size, height=self.size, align = 'center')
        # drawCircle(self.x, self.y, self.size, fill = 'red')

    def checkCollision(self, bullet):
        distanceSquared = (self.x - bullet.x) ** 2 + (self.y - bullet.y) ** 2
        return distanceSquared <= (self.size / 2) ** 2
    
# power-up class 
class PowerUp:
    def __init__(self, x, y, size=20, effect="shield"):
        self.x = x
        self.y = y
        self.size = size
        self.effect = effect
        self.active = True

    def draw(self):
        if self.effect == "shield":
            drawCircle(self.x, self.y, self.size, fill='blue', opacity=70)
            drawCircle(self.x, self.y, self.size - 4, fill=None, border='white', borderWidth=2)
        elif self.effect == "gravityInverter":
            drawCircle(self.x, self.y, self.size, fill='purple', opacity=70)
            drawPolygon(self.x - 5, self.y + 5, self.x + 5, self.y + 5, self.x, self.y - 7, fill='white')
        elif self.effect == "speedBoost":
            drawCircle(self.x, self.y, self.size, fill='aqua', opacity=70)
            drawPolygon(self.x - 5, self.y - 5, self.x + 2, self.y, self.x - 5, self.y + 5, fill='yellow')

    def checkCollision(self, player):
        distance = math.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2)
        return distance <= self.size + player.width / 2

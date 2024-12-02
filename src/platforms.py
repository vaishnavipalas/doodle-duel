from cmu_graphics import *
from settings import GameSettings, Images

# Platform class
class Platform:
    def __init__(self, x, y, image, hasSpring=False):
        self.x = x
        self.y = y
        self.width = GameSettings.platformWidth
        self.height = GameSettings.platformHeight
        self.hasSpring = hasSpring
        if hasSpring == True:
            self.image = Images.platformWithSpring
        else:
            self.image = image

    def draw(self):
        if self.hasSpring == False:
            drawImage(self.image, self.x, self.y, width=self.width, height=self.height)
        else:
            drawImage(self.image, self.x, self.y, width=self.width+10, height=self.height+20)
from cmu_graphics import *
from settings import GameSettings, Images

# Platform class
class Platform:
    def __init__(self, x, y, image, hasSpring=False, isMoving=False):
        self.x = x
        self.y = y
        self.width = GameSettings.platformWidth
        self.height = GameSettings.platformHeight
        
        # platform with a spring
        self.hasSpring = hasSpring
        if hasSpring == True:
            self.image = Images.platformWithSpring
        elif isMoving == True:
            self.image = Images.movingPlatformImage
        else:
            self.image = image

        # moving platform
        self.isMoving = isMoving
        self.moveDirection = 1
        self.moveSpeed = 5

    def __repr__(self):
        return f'Platform at ({self.x}, {self.y})'

    # if isMoving
    def move(self, leftEdge, rightEdge):
        if self.isMoving:
            self.x += self.moveDirection * self.moveSpeed
            # platform should move back and forth
            if self.x <= leftEdge or self.x + self.width >= rightEdge:
                self.moveDirection *= -1


    def draw(self):
        if self.hasSpring == True: # dimensions are different for spring image
            drawImage(self.image, self.x, self.y, width=self.width+10, height=self.height+20)
        else:
            drawImage(self.image, self.x, self.y, width=self.width, height=self.height)
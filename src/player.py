from cmu_graphics import *
from settings import GameSettings, Images

# Player class
class Player:
    def __init__(self, x, y, imageName):
        self.x = x
        self.y = y
        self.width = GameSettings.playerWidth
        self.height = GameSettings.playerHeight
        self.image = imageName
        self.vy = 0
        self.jumping = False
        self.score = 0
        self.direction = None
        self.ghostY = y

    def move(self, leftEdge, rightEdge):
        if self.direction == 'left':
            self.image = Images.leftDoodler
            self.x -= 6
            if self.x + self.width <= leftEdge:
                self.x = rightEdge - self.width
        elif self.direction == 'right':
            self.image = Images.rightDoodler
            self.x += 6
            if self.x - self.width >= rightEdge:
                self.x = leftEdge

    def applyGravity(self):
        self.vy += GameSettings.gravity
        self.y += self.vy
        self.ghostY += self.vy

    def jump(self):
        self.vy = GameSettings.jumpStrength
        self.jumping = True

    def draw(self, mirror=False, offsetSign = 1):
        drawImage(self.image, self.x, self.y + GameSettings.playerHeight // 2, 
                    align='center',
                  width=GameSettings.playerWidth, height=GameSettings.playerHeight)
        # draw clone
        drawImage(self.image, self.x + offsetSign * GameSettings.offset, self.ghostY + GameSettings.playerHeight // 2,
              align='center', width=self.width, height=self.height, opacity = 50)
from cmu_graphics import *
from settings import *

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
        self.gravity = 2
        self.jumpStrength = -35
        self.maxVerticalReach = self.jumpStrength / self.gravity
        self.maxHorizontalReach = self.jumpStrength * 1.5 

        # for power-ups
        self.shieldActive = False
        self.shieldTimer = 0
        self.gravityActive = False
        self.gravityTimer = 0
        self.speedBoostActive = False
        self.speedBoostTimer = 0
        self.speed = 10
        

    def applyPowerUp(self, app):
        if self.shieldActive:
            self.shieldTimer -= 1
            if self.shieldTimer <= 0:
                self.shieldActive = False
        if self.gravityActive:
            self.gravityTimer -= 1
            if self.gravityTimer == 0:
                self.gravity = 2
                self.gravityActive = False
        elif self.speedBoostActive:
            self.speedBoostTimer -= 1
            if self.speedBoostTimer <= 0:
                self.speed = 10
                self.speedBoostActive = False


    def move(self, leftEdge, rightEdge):
        if self.direction == 'left':
            self.image = Images.leftDoodler
            self.x -= self.speed
            if self.x + self.width <= leftEdge:
                self.x = rightEdge - self.width
        elif self.direction == 'right':
            self.image = Images.rightDoodler
            self.x += self.speed
            if self.x - self.width >= rightEdge:
                self.x = leftEdge

    def applyGravity(self):
        if self.speedBoostActive:
            self.gravity = 1.5
        self.vy += self.gravity
        self.y += self.vy
        self.ghostY += self.vy

    def jump(self):
        self.vy = self.jumpStrength
        self.jumping = True

    def draw(self, mirror = False, offsetSign = 1):
        thickness = 20 if self.speedBoostActive == True else 0
        
        if self.gravityActive == True or self.speedBoostActive == True:
            drawCircle(self.x, self.y+15, 70, fill = 'white', opacity = 50)
        
        drawImage(self.image, self.x, self.y + GameSettings.playerHeight // 2, 
                    align='center',
                  width=GameSettings.playerWidth, height=GameSettings.playerHeight, borderWidth = thickness)
        
        
        if self.shieldActive == True:
            drawCircle(self.x, self.y+15, 80, fill = 'blue', opacity = 10)
        

        # draw clone
        drawImage(self.image, self.x + offsetSign * GameSettings.offset, self.ghostY + GameSettings.playerHeight // 2,
              align='center', width=self.width, height=self.height, opacity = 50)
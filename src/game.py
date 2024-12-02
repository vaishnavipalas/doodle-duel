from cmu_graphics import *
import random
import math
from settings import GameSettings, Images, Sounds

from player import Player
from platforms import Platform
from objects import BlackHole, Bullet

# Game class
class Game:
    def __init__(self, leftEdge, seed, isAI = False):
        # game state
        self.isAI = isAI # determine if AI controlled
        self.randomGen = random.Random(seed) # random number generation with seed for consistency
        self.leftEdge = leftEdge
        self.rightEdge = leftEdge + GameSettings.gameWidth
        self.gameOver = False

        # initialize platforms (regular and broken)
        firstPlatform = Platform(leftEdge + 125, 500, Images.platformImage)
        self.platforms = [firstPlatform] + [Platform(self.randomGen.randint(leftEdge, self.rightEdge - GameSettings.platformWidth), y, Images.platformImage, 
                        hasSpring=(self.randomGen.random() < 0.1)) # 10% chance of the platform having a spring
                        for y in range(70, 500, GameSettings.platformSpacing)
                        ]
        self.brokenPlatforms = [Platform(self.randomGen.randint(self.leftEdge, self.rightEdge - GameSettings.platformWidth), y, Images.brokenPlatformImage)
                                for y in range(70, 500, GameSettings.platformSpacing * 3)
                            ]

        # initialize black holes
        self.blackHoles = []
        self.lastBlackHoleScore = -1

        # create player (and bullets)
        self.player = Player(leftEdge + 150, 400, Images.rightDoodler)
        self.bullets = []

    def checkCollisionsWithPlatforms(self, app):
        player = self.player
        if player.vy > 0:
            for platforms in (self.platforms, self.brokenPlatforms):
                for platform in platforms:
                    if (player.y + player.height >= platform.y and player.y <= platform.y + platform.height and
                        player.x + player.width > platform.x and player.x < platform.x + platform.width):
                        if platform in self.brokenPlatforms:
                            self.brokenPlatforms.remove(platform)
                            Sound(Sounds.breakingPlatformSound).play()
                        elif platform.hasSpring:
                            player.vy = -30
                            Sound(Sounds.springSound).play()
                        else:
                            player.jump()
                            Sound(Sounds.jumpSound).play()

    def generateNewPlatforms(self):
        lastPlatformY = self.platforms[-1].y
        lastBrokenY = self.brokenPlatforms[-1].y

        # Generate a new platform if conditions are met
        if lastPlatformY >= GameSettings.platformSpacing:
            newPlatformX = self.randomGen.randint(self.leftEdge, self.rightEdge - GameSettings.platformWidth)
            newPlatformY = 0
            self.platforms.append(Platform(newPlatformX, newPlatformY, Images.platformImage, 
                                        hasSpring=(self.randomGen.random() < 0.1)))

        # Generate a new broken platform if conditions are met
        if lastBrokenY >= GameSettings.platformSpacing * 2.25:
            newBrokenX = self.randomGen.randint(self.leftEdge, self.rightEdge - GameSettings.platformWidth)
            newBrokenY = 0
            self.brokenPlatforms.append(Platform(newBrokenX, newBrokenY, Images.brokenPlatformImage))

        # Remove platforms that are out of view
        self.platforms = [p for p in self.platforms if p.y < GameSettings.gameHeight]
        self.brokenPlatforms = [p for p in self.brokenPlatforms if p.y < GameSettings.gameHeight]


    def generateBlackholes(self):
        # Generate a new black hole periodically
        if self.player.score % 1000 == 0 and self.player.score != self.lastBlackHoleScore:
            newBlackholeX = self.randomGen.randint(self.leftEdge, self.rightEdge - GameSettings.platformWidth)
            newBlackholeY = 0
            self.blackHoles.append(BlackHole(newBlackholeX, newBlackholeY))
            self.lastBlackHoleScore = self.player.score
        # get rid of blackholes out of view
        newBlackholes = []
        for p in self.blackHoles:
            if p.y < GameSettings.gameHeight:
                newBlackholes.append(p)
        self.blackHoles = newBlackholes
        # check if player hits it
        for hole in self.blackHoles:
            if self.detectCollisionWithBlackHole(self.player, hole):
                Sound(Sounds.trapSound).play()
                self.gameOver = True

    # Helper method for collision detection
    def detectCollisionWithBlackHole(self, player, blackHole):
        playerLeft = player.x - player.width // 2
        playerRight = player.x + player.width // 2
        playerTop = player.y - player.height // 2
        playerBottom = player.y + player.height // 2
        
        holeLeft = blackHole.x - blackHole.size // 2
        holeRight = blackHole.x + blackHole.size // 2
        holeTop = blackHole.y - blackHole.size // 2
        holeBottom = blackHole.y + blackHole.size // 2

        # Check if player overlaps with the black hole
        return not (playerRight < holeLeft or playerLeft > holeRight or 
                    playerBottom < holeTop or playerTop > holeBottom)

    def shootBullets(self):
        for i in range(10):
            angle = (math.pi / 5) * i - math.pi / 2
            bullet = Bullet(self.player.x, self.player.y)
            bullet.dx = math.cos(angle) * 5 
            bullet.dy = math.sin(angle) * -5
            self.bullets.append(bullet)

    def updateBullets(self):
        newBullets = []
        for bullet in self.bullets:
            bullet.move()
            if bullet.y > 0:
                newBullets.append(bullet)
        self.bullets = newBullets

    def drawBullets(self):
        for bullet in self.bullets:
            bullet.draw()

    def shiftView(self, otherPlayer):
        # adjust position of objects on the screen based on the players relative position
        if self.player.y < GameSettings.gameHeight // 2:
            shift = GameSettings.gameHeight // 2 - self.player.y
            self.player.score += shift
            
            for platform in self.platforms:
                platform.y += shift

            for broken in self.brokenPlatforms:
                broken.y += shift

            for hole in self.blackHoles:
                hole.y += shift

            # Reset player position
            self.player.y = GameSettings.gameHeight // 2

            # adjust the y coordinate of the ghost
            if otherPlayer:
                otherPlayer.ghostY += shift

    def controlAI(self):
        # initialize 'best' variables to calculate the nearest platform
        nearestPlatform = None
        smallestVerticalDistance = None

        # iterate through all platforms to find the platform with the smallest vertical distance (nearest)
        for platform in self.platforms:
            # Calculate the vertical distance between the player and the platform
            distance = abs(platform.y - self.player.y)
            
            # update 'best' variable
            if smallestVerticalDistance == None or distance < smallestVerticalDistance:
                smallestVerticalDistance = distance
                nearestPlatform = platform
        
        # check horizontal distance to nearest platform
        platformCenterX = nearestPlatform.x + nearestPlatform.width // 2
        horizontalDistance = abs(platformCenterX - self.player.x)

        # if the platform is too far, use wraparound
        if horizontalDistance > GameSettings.gameWidth // 2:
            if platformCenterX < self.player.x: # if it's to the left
                self.player.x = 0
            else: # if it's to the right
                self.player.x = GameSettings.gameWidth
            self.player.direction = None
        else:
            # movement towards platform
            if platformCenterX < self.player.x:
                self.player.direction = 'left'
            elif platformCenterX > self.player.x:
                self.player.direction = 'right'
            else:
                self.player.direction = None  # No horizontal movement if aligned

    def update(self, app, otherPlayer=None):
        if not self.gameOver:
            if self.isAI:
                self.controlAI()
            self.player.move(self.leftEdge, self.rightEdge)
            self.player.applyGravity()
            self.checkCollisionsWithPlatforms(app)
            self.shiftView(otherPlayer)
            self.generateNewPlatforms()
            # self.generateBlackholes()
            self.updateBullets()

            if self.player.y > GameSettings.gameHeight:
                self.gameOver = True
                Sound(Sounds.fallingSound).play()

    def draw(self, mirror = False):
        drawRect(self.leftEdge, 0, GameSettings.gameWidth, 30, fill='lightBlue', opacity=70)
        if self.blackHoles:
            for blackhole in self.blackHoles:
                blackhole.draw()
        self.player.draw(mirror = mirror, offsetSign = -1 if mirror else 1)
        self.drawBullets()
        for platform in self.platforms:
            platform.draw()
        for platform in self.brokenPlatforms:
            platform.draw()
        drawLabel(f'{self.player.score}', self.leftEdge + 15, 15, align='left', size=20, bold=True)

class BackgroundManager:

    @staticmethod
    def drawDefault():
        drawRect(0, 0, GameSettings.gameWidth*2, GameSettings.gameHeight*2, fill = 'white')

    @staticmethod
    def drawSpace(app):
        drawRect(0, 0, app.width, app.height, fill='darkBlue')
        for _ in range(100):
            x =random.randint(0, app.width)
            y = random.randint(0, app.height)
            r = random.randint(1, 3)
            drawCircle(x, y, r, fill='white')    
        # planet 1
        drawCircle(100, 500, 50, fill='purple')
        drawCircle(100, 500, 45, fill='blue')
        drawCircle(100, 500, 40, fill='purple')
        # planet 2
        drawCircle(300, 200, 40, fill='orange')
        drawCircle(290, 190, 10, fill='red')
        # planet 3
        drawCircle(700, 400, 50, fill='pink')
        drawCircle(700, 400, 45, fill='yellow')
        drawCircle(700, 400, 40, fill='pink')
        drawOval(700, 400, 190, 20, fill = None, 
                border='gray', opacity=70, rotateAngle = -40) 
        drawOval(700, 400, 180, 15, fill = None, 
                border='silver', opacity=70, rotateAngle = -40) 
        drawOval(700, 400, 170, 10, fill = None, 
                border='gray', opacity=70, rotateAngle = -40)  
        drawRect(0, 0, app.width, app.height, fill='darkBlue', opacity = 50)

    @staticmethod
    def drawUnderwater(app):
        # background
        for i in range(app.height):
            blueShade = 255 - int((i / app.height) * 100)  # Darker blue near the bottom
            drawLine(0, i, app.width, i, fill=rgb(0, blueShade, 255), lineWidth=2)

        # draw bubbles
        for _ in range(50):
            x = random.randint(0, app.width)
            y = random.randint(0, app.height)
            r = random.randint(5, 15)  # Random bubble size
            drawCircle(x, y, r, fill=None, border='lightBlue', borderWidth=2, opacity=100)
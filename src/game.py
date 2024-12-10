from cmu_graphics import *
import math
import time
from settings import *
# citation: asked chatgpt how to increase efficency, it told me to import deque
from collections import deque
from player import *
from platforms import *
from objects import *
import copy
import random


# Game class
class Game:
    def __init__(self, leftEdge, seed):        
        # game state
        self.isAI = False # determine if AI controlled
        self.randomGen = random.Random(seed) # random number generation with seed for consistency
        self.leftEdge = leftEdge
        self.rightEdge = leftEdge + GameSettings.gameWidth
        self.gameOver = False
        self.otherGame = None
        self.theme = 'default'
        self.name = ''

        # initialize platforms (regular and broken)
        firstPlatform = Platform(leftEdge + 125, GameSettings.gameHeight - 200, Images.platformImage)
        self.platforms = deque([firstPlatform])
        
        self.brokenPlatforms = [Platform(random.randint(self.leftEdge, self.rightEdge - GameSettings.platformWidth), y, Images.brokenPlatformImage)
                                for y in range(70, GameSettings.gameHeight - 200, GameSettings.platformSpacing * 3)
                            ]

        # initialize objects
        self.blackHoles = deque([])
        self.lastBlackHoleTime = time.time()
        self.monsters = deque([])
        self.lastMonsterSpawnTime = time.time()
        self.powerUps = deque([])
        self.lastPowerTime = time.time()

        # create player (and bullets)
        self.player = Player(leftEdge + 150, 400, Images.rightDoodler)
        self.bullets = deque([])

    def shouldJump(self):
        player = self.player
        if player.vy > 0:
            for platforms in (self.platforms, self.brokenPlatforms):
                for platform in platforms:
                    if (player.y + player.height >= platform.y and player.y <= platform.y + platform.height and
                        (player.x + (player.width // 2)) > platform.x and (player.x - (player.width // 2)) < platform.x + platform.width):
                        if platform in self.brokenPlatforms:
                            self.brokenPlatforms.remove(platform)
                            Sound(Sounds.breakingPlatformSound).play()
                        elif platform.hasSpring:
                            player.vy = player.jumpStrength * 2
                            Sound(Sounds.springSound).play()
                        else:
                            player.jump()
                            Sound(Sounds.jumpSound).play()

    def generateNewPlatforms(self):
        # make sure the platforms are reachable
        # citation: used chatgpt to figure out formula
        maxHeight = (self.player.jumpStrength ** 2) / (2 * self.player.gravity)
        maxSpacingY = min(GameSettings.platformSpacing, maxHeight*0.4)
        
        lastPlatformY = self.platforms[-1].y
        lastBrokenY = self.brokenPlatforms[-1].y

        # generate a new platform
        if lastPlatformY >= maxSpacingY:
            newPlatformX = random.randint(self.leftEdge, self.rightEdge - GameSettings.platformWidth)
            newPlatformY = lastPlatformY - maxSpacingY
            self.platforms.append(Platform(newPlatformX, newPlatformY, Images.platformImage, 
                                        hasSpring=(random.random() < 0.1), isMoving=(random.random() < 0.2)))

        # generate a new broken platform (less often)
        if lastBrokenY >= maxSpacingY * 2.25:
            newBrokenX = random.randint(self.leftEdge, self.rightEdge - GameSettings.platformWidth)
            newBrokenY = lastBrokenY - maxSpacingY*2.25
            self.brokenPlatforms.append(Platform(newBrokenX, newBrokenY, Images.brokenPlatformImage))



    def generateBlackholes(self):
        currTime = time.time()
        # generate a new black hole every 30 seconds
        if currTime - self.lastBlackHoleTime >= 30 and len(self.blackHoles) == 0:
            newBlackholeX = random.randint(self.leftEdge, self.rightEdge - GameSettings.platformWidth)
            newBlackholeY = 0
            self.blackHoles.append(BlackHole(newBlackholeX, newBlackholeY))
            self.lastBlackHoleTime = currTime
        # check if player hits it
        for hole in self.blackHoles:
            if self.detectCollisionWithBlackHole(self.player, hole):
                Sound(Sounds.trapSound).play()
                self.gameOver = True
                self.otherGame.gameOver = True

    def detectCollisionWithBlackHole(self, player, blackHole):
        # the center positions of the player and the black hole
        playerCenterX = player.x
        playerCenterY = player.y
        blackHoleCenterX = blackHole.x
        blackHoleCenterY = blackHole.y

        # radius of the player and the black hole
        playerRadius = min(player.width, player.height) // 2
        blackHoleRadius = blackHole.size // 2

        # distance formula between the centers of the player and the black hole
        distance = math.sqrt((playerCenterX - blackHoleCenterX) ** 2 + 
                            (playerCenterY - blackHoleCenterY) ** 2)

        return distance < (playerRadius + blackHoleRadius)

    def shootBullets(self):
        Sound(Sounds.shootBulletSound).play()
        bullet = Bullet(self.player.x, self.player.y)
        if len(self.bullets) < 7:
            self.player.image = Images.doodleShootingImage
            self.bullets.append(bullet)
            self.player.image = Images.rightDoodler

    def monsterLogic(self, app):
        currTime = time.time()

        # spawn monster every 15 seconds
        if currTime - self.lastMonsterSpawnTime >= 15 and len(self.monsters) == 0:
            x = random.randint(self.leftEdge, self.rightEdge - 40)  # Monster size consideration
            y = -400  # spawn ahead
            newMonster = Monster(x, y)
            self.monsters.append(newMonster)
            self.lastMonsterSpawnTime = currTime

            # 50/50 chance of generating a shield for the player if there is a monster
            if random.random() < 0.5:
                shieldX = random.randint(self.leftEdge, self.rightEdge - 40)
                shieldY = 0
                newShield = PowerUp(shieldX, shieldY, size=20, effect="shield")
                self.powerUps.append(newShield)

        i = 0
        while i < len(self.monsters):
            monster = self.monsters[i]
            collided = False
            for bullet in self.bullets:
                if monster.checkCollision(bullet):
                    Sound(Sounds.trapSound).play()
                    self.bullets.remove(bullet)
                    collided = True

            # check if monster collides with the player
            distance = math.sqrt((self.player.x - monster.x) ** 2 + (self.player.y - monster.y) ** 2)
            if not self.player.shieldActive and distance <= (self.player.width / 2 + monster.size / 2):
                self.gameOver = True
                self.otherGame.gameOver = True
                Sound(Sounds.fallingSound).play()
                break

            if collided:
                self.monsters.pop(i)
            else:
                i += 1


    def generatePowerUps(self):
        currTime = time.time()
        
        if currTime - self.lastPowerTime >= 20:
            x = random.randint(self.leftEdge, self.rightEdge)
            y = 0  # Spawn at the top of the screen
            if self.theme == "space":
                effect = "gravityInverter"
            elif self.theme == "underwater":
                effect = "speedBoost"
            self.powerUps.append(PowerUp(x, y, effect=effect))
            self.lastPowerTime = currTime

    def checkHitPowerUp(self):
        for powerUp in self.powerUps:
            if powerUp.checkCollision(self.player):
                Sound(Sounds.grabPowerUpSound).play()
                if powerUp.effect == "shield":
                    self.player.shieldActive = True
                    self.player.shieldTimer = 240
                elif powerUp.effect == "gravityInverter" and self.theme == "space":
                    self.player.gravityActive = True
                    self.player.gravity = 0.5
                    self.player.gravityTimer = 300
                elif powerUp.effect == "speedBoost" and self.theme == "underwater":
                    self.player.speed = 20
                    self.player.speedBoostActive = True
                    self.player.speedBoostTimer = 300
                self.powerUps.remove(powerUp)

    def shiftView(self, otherPlayer):
        # adjust position of objects on the screen based on the players relative position
        if self.player.y < GameSettings.gameHeight // 2:
            shift = GameSettings.gameHeight // 2 - self.player.y
            self.player.score += shift
            self.player.y = GameSettings.gameHeight // 2
            for objects in [self.platforms, self.brokenPlatforms, self.blackHoles, self.monsters, self.powerUps]:
                for object in objects:
                    object.y += shift

            # adjust the y coordinate of the ghost
            if otherPlayer:
                otherPlayer.ghostY += shift

    def cleanup(self):
        self.platforms = [p for p in self.platforms if p.y < GameSettings.gameHeight]
        self.brokenPlatforms = [p for p in self.brokenPlatforms if p.y < GameSettings.gameHeight]
        self.monsters = [m for m in self.monsters if m.y < GameSettings.gameHeight]
        self.powerUps = [pu for pu in self.powerUps if pu.y < GameSettings.gameHeight]
        self.blackHoles = [bh for bh in self.blackHoles if bh.y < GameSettings.gameHeight]
        self.bullets = [b for b in self.bullets if b.y > 0]

    '''
    AI COMPONENT
    '''
    def controlAI(self):
        # recursive function to evalaute the best target for the AI; use wrapper function
        def findTarget(targets, index=0, best=None):
            maxHorizontalDistance = 10000
            shootingRange = 150
            powerUpTargetDistance = 250

            if index >= len(targets):
                # base case: return the best target found
                return best
            else:

                target = targets[index]
                if isinstance(target, Platform):
                    horizontalDistance = abs(target.x + target.width // 2 - (self.player.x + self.player.width // 2))
                    wrappedHorizontalDistance = min(horizontalDistance, GameSettings.gameWidth - horizontalDistance)
                    verticalDistance = target.y - self.player.y

                    if verticalDistance > 0:  # only check platforms below the player
                        totalDistance = wrappedHorizontalDistance + (2 * verticalDistance)
                        # citation: used chatGPT to try to debug why the player was favoring moving platforms over static ones
                        if not getattr(target, 'moving', False):
                            totalDistance -= 50
                        else:
                            predictedX = target.x + target.speed * abs(verticalDistance / self.player.jumpSpeed)
                            if abs(predictedX - self.player.x) > maxHorizontalDistance:
                                return findTarget(targets, index + 1, best)

                        if best is None or totalDistance < best[1]:
                            best = (target, totalDistance)

                elif isinstance(target, Monster):
                    horizontalDistance = abs(target.x + target.size//2 - (self.player.x + self.player.width // 2))
                    verticalDistance = target.y - self.player.y

                    if target.y >= 0 and horizontalDistance <= shootingRange and verticalDistance < -300:
                        totalDistance = horizontalDistance + verticalDistance
                        if best is None or totalDistance < best[1]:
                            best = (target, totalDistance)

                elif isinstance(target, (Monster, BlackHole)):
                    horizontalDistance = abs(target.x - self.player.x)
                    verticalDistance = abs(target.y - self.player.y)
                    totalDistance = horizontalDistance + verticalDistance
                    if best is None or totalDistance < best[1]:
                        best = (target, totalDistance)

                elif isinstance(target, PowerUp):
                    horizontalDistance = abs(target.x - self.player.x)
                    verticalDistance = abs(target.y - self.player.y)
                    if horizontalDistance <= powerUpTargetDistance:
                        totalDistance = horizontalDistance + verticalDistance
                        if best is None or totalDistance < best[1]:
                            best = (target, totalDistance)

                # recursive case: evaluate the next target
                return findTarget(targets, index + 1, best)


        targets = self.platforms + self.monsters + self.blackHoles + self.powerUps

        # find the best target
        best = findTarget(targets)

        if best:
            bestTarget, totalDistance = best

            # determine action based on the best target
            if isinstance(bestTarget, PowerUp):
                if bestTarget.x < self.player.x:
                    self.player.direction = 'left'
                elif bestTarget.x > self.player.x:
                    self.player.direction = 'right'
                else:
                    self.player.direction = None
                return

            elif isinstance(bestTarget, Monster):
                if bestTarget.x < self.player.x:
                    self.player.direction = 'left'
                elif bestTarget.x > self.player.x:
                    self.player.direction = 'right'
                else:
                    self.player.direction = None
                self.shootBullets()
                return

            elif isinstance(bestTarget, (Monster, BlackHole)):
                if bestTarget.x < self.player.x:
                    self.player.direction = 'right'
                else:
                    self.player.direction = 'left'
                return

            elif isinstance(bestTarget, Platform):
                platformCenterX = bestTarget.x + bestTarget.width // 2
                if platformCenterX < self.player.x - 5:
                    self.player.direction = 'left'
                elif platformCenterX > self.player.x + 5:
                    self.player.direction = 'right'
                else:
                    self.player.direction = None
                return
        else:
            # if no target found
            self.player.direction = None


    # check if player is less than game height
    def detectGameOver(self):
        if self.player.y > GameSettings.gameHeight:
            self.gameOver = True
            
            self.otherGame.gameOver = True
            Sound(Sounds.fallingSound).play()


    def moveObjects(self):
        
        for platform in self.platforms:
            if platform.isMoving:
                platform.move(self.leftEdge, self.rightEdge)
        if self.monsters:
            for monster in self.monsters:
                monster.move()
        if self.bullets:
            for bullet in self.bullets:
                bullet.move()

    # update
    def update(self, app, otherPlayer=None):
        if not self.gameOver:
            if self.isAI:
                # control movements with AI
                self.controlAI()

            # update player
            self.player.move(self.leftEdge, self.rightEdge)
            self.player.applyGravity()
            self.detectGameOver()

            # update screen
            self.shiftView(otherPlayer)
            self.moveObjects()
            self.cleanup()

            # objects
            self.shouldJump()
            self.monsterLogic(app)
            self.generateNewPlatforms()
            self.generateBlackholes()
            

            # powerup logic
            if self.theme in ['space', 'underwater']:
                self.generatePowerUps()
            self.checkHitPowerUp()
            self.player.applyPowerUp(app)

    # draw game
    def draw(self, mirror = False):
        for objects in [self.platforms, self.brokenPlatforms, self.monsters, self.blackHoles, self.powerUps, self.bullets]:
            for obj in objects:
                obj.draw()
        self.player.draw(mirror = mirror, offsetSign = -1 if mirror else 1)




# draw backgrounds for themes
class BackgroundManager:

    @staticmethod
    def drawDefault(app):
        drawRect(0, 0, app.width, app.height, fill = 'floralWhite')

        gridSpacing = 20
        lineColor = 'burlyWood'

        # vertical lines
        for x in range(0, app.width, gridSpacing):
            drawLine(x, 0, x, app.height, fill=lineColor, opacity=20)

        # horizontal lines
        for y in range(0, app.height, gridSpacing):
            drawLine(0, y, app.width, y, fill=lineColor, opacity=20)

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
        color = gradient('lightBlue', 'darkBlue', start = 'top')
        drawRect(0, 0, app.width, app.height, fill = color)

        # draw bubbles
        for _ in range(25):
            x = random.randint(0, app.width)
            y = random.randint(0, app.height)
            r = random.randint(5, 15)  # Random bubble size
            drawCircle(x, y, r, fill=None, border='lightBlue', borderWidth=2, opacity=70)
        drawRect(0, 0, app.width, app.height, fill = 'lightBlue', opacity = 20)
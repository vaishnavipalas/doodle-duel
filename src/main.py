# Note: graphics/sounds cited in settings.py

from cmu_graphics import *
import random
import math
from settings import GameSettings, Images, Sounds
from game import Game, BackgroundManager

# functions to create instances of the game class
def restart1(app, seed):
    app.gameArrows = Game(GameSettings.gameWidth + 50, seed)

def restart2(app, seed):
    app.gameWASD = Game(0, seed, isAI = True)

def startGame(app):
    seed = random.randint(1, 100)
    restart1(app,seed)
    restart2(app, seed)


# --------------APP FUNCTIONS-------------------------------
def onAppStart(app):
    app.started = False
    app.paused = False
    app.time = 0
    app.bgType = 'default'  # Default background

def onMousePress(app, mouseX, mouseY):
    if not app.started:
        # Background selection buttons
        if (app.width // 2 - 150) <= mouseX <= (app.width // 2 - 50) and 250 <= mouseY <= 350:
            app.bgType = 'default'
        elif (app.width // 2 - 50) <= mouseX <= (app.width // 2 + 50) and 250 <= mouseY <= 350:
            app.bgType = 'space'
        elif (app.width // 2 + 50) <= mouseX <= (app.width // 2 + 150) and 250 <= mouseY <= 350:
            app.bgType = 'underwater'
        # Start button
        elif (app.width // 2 - 100) <= mouseX <= (app.width // 2 + 100) and 385 <= mouseY <= 425:
            app.started = True
            startGame(app)
            Sound(Sounds.startSound).play()
    else:
        # Pause button
        if GameSettings.gameWidth <= mouseX <= GameSettings.gameWidth + 40 and 10 <= mouseY <= 50:
            app.paused = not app.paused

def onKeyPress(app, key):
    if not app.paused:
        if key == 'up':
            app.gameArrows.player.image = Images.doodleShootingImage
            app.gameArrows.shootBullets()
        if key == 'left':
            app.gameArrows.player.direction = 'left'
        elif key == 'right':
            app.gameArrows.player.direction = 'right'
        if key == 'w':
            app.gameWASD.player.image = Images.doodleShootingImage
            app.gameWASD.shootBullets()
        if key == 'a':
            app.gameWASD.player.direction = 'left'
        elif key == 'd':
            app.gameWASD.player.direction = 'right'

        if app.gameArrows.gameOver and key == 'space':
            restart1(app)
        if app.gameWASD.gameOver and key == 'space':
            restart2(app)
        if key == '[':
            app.started = False

def onKeyRelease(app, key):
    if not app.paused:
        if key in ('left', 'right'):
            app.gameArrows.player.direction = None
        if key in ('a', 'd'):
            app.gameWASD.player.direction = None
        if key in ('w', 'up'):
            app.gameArrows.player.image = Images.rightDoodler
            app.gameWASD.player.image = Images.rightDoodler

def onStep(app):
    app.time += 1
    if app.paused == False and app.started == True:
        app.gameArrows.update(app, app.gameWASD.player)
        app.gameWASD.update(app, app.gameArrows.player)

# --------------DRAW FUNCTIONS--------------------
def drawPauseButton(app):
    drawRect(GameSettings.gameWidth, 30, 50, 40, fill='lightGray', border='black', align='left')
    if not app.paused:
        pauseText = 'Pause'
    else:
        pauseText = 'Resume'
    drawLabel(pauseText, GameSettings.gameWidth + 25, 30, size=12, align='center', bold=True)

def drawGameOver(game):
    drawRect(game.leftEdge, 0, GameSettings.gameWidth, GameSettings.gameHeight, fill = 'white')
    drawLabel("Game Over!", game.leftEdge + (GameSettings.gameWidth // 2), GameSettings.gameHeight // 2 - 60, size=50, bold=True, fill='black')
    drawLabel(f"Your Score: {game.player.score}", game.leftEdge + (GameSettings.gameWidth // 2), GameSettings.gameHeight // 2, size=30, fill='black')
    drawLabel("Press space bar to restart", game.leftEdge + (GameSettings.gameWidth // 2), GameSettings.gameHeight // 2 + 80, size=20, italic=True, fill='black')

def startScreen(app):
    drawLabel('2-Player Doodle Jump!', app.width / 2, app.height / 2 - 100, size=40, bold=True)
    drawLabel(f'Theme: {app.bgType}', app.width - 60, 20)

    # Background selection buttons
    drawRect(app.width // 2 - 150, 300, 100, 50, 
            fill='lightGray', border='black', align='left')
    drawLabel('Default', app.width // 2 - 100, 300, size=14, align='center')
    drawRect(app.width // 2 - 50, 300, 100, 50, 
            fill='lightGray', border='black', align='left')
    drawLabel('Space', app.width // 2, 300, size=14, align='center')
    drawRect(app.width // 2 + 50, 300, 100, 50, 
            fill='lightGray', border='black', align='left')
    drawLabel('Underwater', app.width // 2 + 100, 300, size=14, align='center')

    # Start button
    drawRect(app.width // 2, 400, 200, 50, align='center', fill='gray', border='black')
    drawLabel('Start Game', app.width / 2, 400, size=20, bold=True)

    # Add a jumping doodle
    doodleY = 400 + (40 * math.sin(app.time / 10))  # bounce
    drawImage(Images.leftDoodler, 200, doodleY, align='center', width=100, height=100)
    drawImage(Images.platformImage, 180, 500, align='center', width=100, height=30)

def drawBackground(app):
    if app.bgType == 'default':
        BackgroundManager.drawDefault()
    elif app.bgType == 'space':
        BackgroundManager.drawSpace(app)
    elif app.bgType == 'underwater':
        BackgroundManager.drawUnderwater(app)
# --------------------------------------


def redrawAll(app):
    if not app.started:
        startScreen(app)
    else:
        if app.paused:
            drawLabel('Game Paused', app.width / 2, app.height / 2, size=40, bold=True, fill='red')
            drawLabel(f'Player1: {app.gameWASD.player.score}      Player2: {app.gameArrows.player.score}', 
                        app.width / 2, app.height / 2 + 40, size=20)
        else:
            drawBackground(app)  # Draw the selected background
            if not app.gameArrows.gameOver:
                app.gameArrows.draw(mirror = True)
            else:
                drawGameOver(app.gameArrows)
            if not app.gameWASD.gameOver:
                app.gameWASD.draw()
            else:
                drawGameOver(app.gameWASD)
            drawRect(GameSettings.gameWidth, 0, 50, GameSettings.gameHeight, fill='gray')
        drawPauseButton(app)

runApp(width=850, height=600)
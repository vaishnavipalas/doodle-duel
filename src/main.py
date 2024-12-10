# Note: graphics/sounds cited in settings.py

from cmu_graphics import *
import math
from settings import *
from game import *
import random

# Citation: outline for Button Class from ChatGPT
class Button:
    def __init__(self, centerX, centerY, width, height, label, onClick):
        self.centerX = centerX
        self.centerY = centerY
        self.width = width
        self.height = height
        self.label = label
        self.onClick = onClick

    def isClicked(self, mouseX, mouseY):
        # distance formula to determine if within button bounds
        dx = abs(mouseX - self.centerX)
        dy = abs(mouseY - self.centerY)
        return dx <= self.width / 2 and dy <= self.height / 2

    def draw(self):
        drawRect(self.centerX - self.width / 2, self.centerY - self.height / 2,
                 self.width, self.height, fill='beige', opacity = 70, border='black')
        drawLabel(self.label, self.centerX, self.centerY, size=0.40*self.height, 
                  align='center', font = 'DoodleJump', bold = True)
        

def drawInstructions(app):
    title = "how to play"

    instructions = [
        "1. use arrow keys to move your character left or right.",
        "2. jump on platforms to gain height and avoid falling.",
        "3. collect power-ups for special abilities:",
        "   - shield: protects you from monsters.",
        "   - speed boost: available in underwater theme, it will increase speed.",
        "   - gravity inverter: available in space theme, it will decrease gravity.",
        "4. avoid monsters and black holes. or, shoot monsters using 'up' or 'a'.",
        "*the game will slow down to warn you of a monster approaching*",
        "5. score points by climbing higher and surviving longer.",
        "6. you can either play with a friend or against an ai by selecting the mode.",
    ]

    controls = [
        "controls:",
        "left player: use 'a' and 'd' to move left/right and 'w' to shoot bullets.",
        "right player: use 'left' and 'right' to move left/right and 'up' to shoot bullets.",
    ]

    themeNotes = [
        "themes:",
        "- default: regular gameplay.",
        "- space: gravity inverter power-up.",
        "- underwater: speed boost power-up.",
    ]

    drawRect(0, 0, app.width, app.height, fill='floralWhite')
    BackgroundManager.drawDefault(app)
    drawLabel(title, app.width // 2, 100, size=60, fill='darkRed', bold=True, font='DoodleJump')

    yStart = 200
    lineSpacing = 30
    for line in instructions:
        drawLabel(line, app.width // 2, yStart, size=20, fill='black', align='center', font='DoodleJump')
        yStart += lineSpacing

    yStart += 30
    for line in controls:
        drawLabel(line, app.width // 2, yStart, size=20, fill='black', align='center', font='DoodleJump')
        yStart += lineSpacing

    yStart += 30
    for line in themeNotes:
        drawLabel(line, app.width // 2, yStart, size=20, fill='black', align='center', font='DoodleJump')
        yStart += lineSpacing

    drawLabel("press 'i' to go back to menu", 
              app.width // 2, 
              app.height - 50, 
              size=22, 
              fill='darkRed', 
              font='DoodleJump')


# Functions to create instances of the game class

def startGame(app):
    seed = random.randrange(1, 100)
    app.secondGame = Game(GameSettings.gameWidth + 50, seed)
    app.firstGame = Game(0, seed)
    app.startTime = time.time()
    app.secondGame.otherGame = app.firstGame
    app.firstGame.otherGame = app.secondGame
    app.firstGame.theme = app.secondGame.theme = app.theme
    app.firstGame.name = app.playerNames[0]
    app.secondGame.name = app.playerNames[1]

# --------------APP FUNCTIONS-------------------------------
def onAppStart(app):
    app.started = False
    app.paused = False
    app.time = 0
    app.theme = 'default'
    app.playerMode = 'friend'
    app.nameInput = False
    app.playerNames = ['', '']
    app.currentNameInput = 0
    app.instructions = False
    

    # Initialize buttons
    app.themeButtonsY = app.height // 2 + 160
    app.modeButtonsY = app.height // 2 + 50
    app.pauseScreenButtonsY = 2 * app.height // 3
    
    app.buttonsBeforeStart = [
        Button(app.width // 2 - 100, app.themeButtonsY, 100, 50, "default", lambda: setTheme(app, "default")),
        Button(app.width // 2, app.themeButtonsY, 100, 50, "space", lambda: setTheme(app, "space")),
        Button(app.width // 2 + 100, app.themeButtonsY, 100, 50, "underwater", lambda: setTheme(app, "underwater")),
        Button(app.width // 2 - 75, app.modeButtonsY, 150, 50, "player vs. player", lambda: setMode(app, "friend")),
        Button(app.width // 2 + 75, app.modeButtonsY, 150, 50, "AI vs. player", lambda: setMode(app, "AI")),
        Button(2 * app.width // 4, app.themeButtonsY + 125, 200, 100, "play", lambda: startNameInput(app)),
    ]

    app.pauseButton = Button(app.width // 2, 40, 70, 50, 'pause', lambda: pauseLogic(app))
    app.newGameButton = Button(app.width // 3, app.pauseScreenButtonsY, 200, 100, 'menu', lambda: newGame(app))
    app.restartGameButton = Button(2 * app.width // 3, app.pauseScreenButtonsY, 200, 100, 'rematch', lambda: restartGame(app))

def restartGame(app):
    app.started = True
    app.instructions = False
    startGame(app)
    Sound(Sounds.startSound).play()

def startNameInput(app):
    app.nameInput = True
    app.playerNames = ['', '']
    app.currentNameInput = 0

def pauseLogic(app):
    app.paused = not app.paused

def setTheme(app, theme):
    app.theme = theme

def setMode(app, mode):
    app.playerMode = mode

def newGame(app):
    app.started = False
    app.paused = False
    app.instructions = False
    app.playerNames = ['', '']  # Reset player names
    app.nameInput = False

def startGameWithSound(app):
    app.started = True
    app.instructions = False
    app.nameInput = False
    startGame(app)
    Sound(Sounds.startSound).play()

def onMousePress(app, mouseX, mouseY):
    if not app.started:
        for button in app.buttonsBeforeStart:
            if button.isClicked(mouseX, mouseY):
                button.onClick()
    else:
        for button in [app.pauseButton, app.newGameButton]:
            if button.isClicked(mouseX, mouseY):
                button.onClick()

        if app.firstGame.gameOver and app.secondGame.gameOver:
            if app.restartGameButton.isClicked(mouseX, mouseY):
                app.restartGameButton.onClick()

def onKeyPress(app, key):
    if not app.started:
        if key == 'i':
            app.instructions = not app.instructions
        if app.nameInput:
            if key == 'enter': # either move on to next game or start game
                if app.playerMode == 'friend':
                    if app.currentNameInput == 0:
                        app.currentNameInput = 1
                    else:
                        startGameWithSound(app)
                else:
                    startGameWithSound(app)
            if key == 'backspace': # backspace
                app.playerNames[app.currentNameInput] = app.playerNames[app.currentNameInput][:-1]
                if app.playerMode == 'AI':
                    if key == 'backspace': # backspace
                        app.playerNames[1] = app.playerNames[1][:-1]
            elif len(key) == 1:
                # add the key to name
                if app.playerMode == 'AI':
                    app.playerNames[1] += key
                else:
                    app.playerNames[app.currentNameInput] += key
    elif not app.paused:
        if key == 'up':
            app.secondGame.player.image = Images.doodleShootingImage
            app.secondGame.shootBullets()
        if key == 'left':
            app.secondGame.player.direction = 'left'
        elif key == 'right':
            app.secondGame.player.direction = 'right'
        if app.firstGame.isAI == False:
            if key == 'w':
                app.firstGame.player.image = Images.doodleShootingImage
                app.firstGame.shootBullets()
            if key == 'a':
                app.firstGame.player.direction = 'left'
            elif key == 'd':
                app.firstGame.player.direction = 'right'

        # shortcut commands for testing/demo
        if key == 'p': # generate power up
            app.firstGame.powerUps.append(PowerUp(200, -20, effect='gravityInverter'))
        if key == 'l': # generate power up
            app.firstGame.powerUps.append(PowerUp(1000, -20, effect='speedBoost'))
        if key == 'm': # generate monster
            app.firstGame.monsters.append(Monster(200, -20))

        if key == 'o': # set game over
            app.firstGame.gameOver = True
            app.secondGame.gameOver = True


def onKeyRelease(app, key):
    if not app.paused and not app.nameInput:
        if key in ('left', 'right'):
            app.secondGame.player.direction = None
        if key in ('a', 'd'):
            app.firstGame.player.direction = None
        if key in ('w', 'up'):
            app.secondGame.player.image = Images.rightDoodler
            app.firstGame.player.image = Images.rightDoodler

def onStep(app):
    app.time += 1
    if app.paused == False and app.started == True:
        app.secondGame.update(app, app.firstGame.player)
        app.firstGame.update(app, app.secondGame.player)

# --------------DRAW FUNCTIONS--------------------

def drawGameOver(app):
    BackgroundManager.drawDefault(app)
    drawLabel("game over!", app.width // 2, app.height // 4, size=80, bold=True, fill='red', font='DoodleJump')
    player1Score = int(app.firstGame.player.score)
    player2Score = int(app.secondGame.player.score)
    if player1Score == player2Score:
        winner = 'draw!'
    elif player1Score > player2Score:
        winner = app.firstGame.name
    else:
        winner = app.secondGame.name
    drawLabel(f'winner: {winner}', app.width // 2, 5 * app.height // 12, size=70, bold=True, font='DoodleJump')
    
    
    drawLabel(f"{app.playerNames[0]}'s score: {player1Score}", app.width // 3, 7 * (app.height // 12), size=40, fill='black', font='DoodleJump')
    drawLabel(f"{app.playerNames[1]}'s score: {player2Score}", 2 * app.width // 3, 7 * (app.height // 12), size=40, fill='black', font='DoodleJump')
    
    app.newGameButton.centerX = app.width // 3
    app.newGameButton.centerY = 3 * app.height // 4
    app.newGameButton.width = 200
    app.newGameButton.height = 100
    app.newGameButton.draw()

    app.restartGameButton.centerX = 2 * app.width // 3
    app.restartGameButton.centerY = 3 * app.height // 4
    app.restartGameButton.width = 200
    app.restartGameButton.height = 100
    app.restartGameButton.draw()

def startScreen(app):
    BackgroundManager.drawDefault(app)
    drawLabel("DOODLE", app.width / 2, app.height / 2 - 290, size=100, fill = 'darkRed', bold=True, font = 'DoodleJump')
    drawLabel("DUEL", app.width / 2, app.height / 2 - 210, size=100, fill = 'darkRed', bold=True, font = 'DoodleJump')
    drawLabel("~ 2-player edition of Doodle Jump ~", app.width / 2, app.height / 2 - 140, size=30, font = 'DoodleJump')
    drawLabel("press 'i' to see instructions", app.width / 2, app.height / 2 - 50, size=25, fill = 'darkRed', font = 'DoodleJump')
    mode = 'player vs. player' if app.playerMode == 'friend' else 'AI vs. player'
    drawLabel(f"theme: {app.theme}", app.width//2, app.themeButtonsY - 50, 
              font = 'DoodleJump', size = 30)
    drawLabel(f"mode: {mode}", app.width//2, app.modeButtonsY - 50, 
              font = 'DoodleJump', size = 30)

    for button in app.buttonsBeforeStart:
        button.draw()


    # Citation: used ChatGPT to draw the jumping doodle on home screen using sinusoidal motion
    doodleY = 500 + (180 * math.sin(app.time / 12))  # bounce
    drawImage(Images.rightDoodler, 300, doodleY, align="right", width=100, height=100)
    drawImage(Images.platformImage, 280, 720, align="right", width=100, height=30)

def drawBackground(app):
    if app.theme == 'default':
        BackgroundManager.drawDefault(app)
    elif app.theme == 'space':
        BackgroundManager.drawSpace(app)
    elif app.theme == 'underwater':
        BackgroundManager.drawUnderwater(app)


def chooseMode(app):
    if app.playerMode == 'friend':
        app.firstGame.isAI = False
    elif app.playerMode == 'AI':
        app.firstGame.isAI = True

def drawBorder(app):
    drawRect(0, 0, app.width, app.height//9, fill='lightBlue', opacity=60)
    drawLine(0, app.height//9, app.width, app.height//9, fill = 'black', lineWidth = 2)
    drawLabel(f'{int(app.firstGame.player.score)}', app.firstGame.leftEdge + 20, app.height//18, 
                    align='left', size=60, bold=True, font = 'DoodleJump')
    drawLabel(f'{int(app.secondGame.player.score)}', app.secondGame.leftEdge + 20, app.height//18, 
                    align='left', size=60, bold=True, font = 'DoodleJump')
    drawLabel(f'{app.playerNames[0]}', app.width // 4, app.height//18, 
                    align='center', size=60, bold=True, font = 'DoodleJump')
    drawLabel(f'{app.playerNames[1]}', 3 * app.width // 4, app.height//18, 
                    align='center', size=60, bold=True, font = 'DoodleJump')

def redrawAll(app):
    if app.nameInput:
        # Draw name input screen
        BackgroundManager.drawDefault(app)
        drawLabel("enter player names", app.width // 2, app.height // 4, size=50, fill = 'darkRed', bold=True, font='DoodleJump')
        if app.playerMode == 'friend':
            for i in range(len(app.playerNames)):
                name = app.playerNames[i]
                prompt = f"player {i + 1} name: {name}" + ("|" if i == app.currentNameInput else "")
                drawLabel(prompt, app.width // 2, app.height // 2 + i * 50, size=30, font='DoodleJump')
        else:
            app.playerNames[0] = 'AI'
            prompt = f"player 2 name: {app.playerNames[1]}" + "|"
            drawLabel(f'player 1 name: {app.playerNames[0]}', app.width // 2, app.height // 2, size=30, font='DoodleJump')
            drawLabel(prompt, app.width // 2, app.height // 2 + 50, size=30, font='DoodleJump')
    elif not app.started:
        startScreen(app)
        if app.instructions:
            drawInstructions(app)
    else:
        drawBackground(app)  # Draw the selected background
        chooseMode(app)
        if not app.secondGame.gameOver and not app.firstGame.gameOver:
            app.secondGame.draw(mirror = True)
            app.firstGame.draw()
            drawRect(app.width//2 - (GameSettings.playerWidth // 2), 0, GameSettings.playerWidth, 1000, fill='gray')
        else:
            drawGameOver(app)
        
        # pause button/screen
        if not app.firstGame.gameOver and not app.secondGame.gameOver:

            if app.paused:
                drawRect(0, 0, app.width, app.height, fill = 'floralWhite', opacity = 80)
                app.pauseButton.label = 'resume'
                app.pauseButton.centerX = 2 * app.width // 3
                app.pauseButton.centerY = app.pauseScreenButtonsY
                app.pauseButton.width = 200
                app.pauseButton.height = 100
                app.pauseButton.draw()
                drawLabel('doodle duel paused', app.width // 2, app.height / 3, size=80, bold=True, fill='red', font = 'DoodleJump')
                app.newGameButton.centerX = app.width // 3
                app.newGameButton.centerY = app.pauseScreenButtonsY
                app.newGameButton.draw()
                drawBorder(app)
            else:
                drawBorder(app)
                app.pauseButton.draw()
                app.pauseButton.label = 'pause'
                app.pauseButton.centerX = app.width // 2
                app.pauseButton.centerY = 40
                app.pauseButton.width = 70
                app.pauseButton.height = 50
                app.newGameButton.centerX = app.width // 2


runApp(width=1440, height=900)
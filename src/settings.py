from cmu_graphics import *

class GameSettings:
    playerWidth = 80
    playerHeight = 80
    platformWidth = 100
    platformHeight = 35
    platformSpacing = 90
    modeButtonWidth = 90
    modeButtonHeight = 40
    gameWidth = 695
    gameHeight = 900
    offset = gameWidth + 50

class Images:
    # Citation: images taken from https://doodlejump.io/ and https://www.bibavonspeyr.com/doodle-jump-8bit 
    platformImage = '../assets/images/doodle-platform.png'
    brokenPlatformImage = '../assets/images/broken-platform.png'
    platformWithSpring = '../assets/images/platform-w-spring.png'
    movingPlatformImage = '../assets/images/moving-platform.png'
    doodleShootingImage = '../assets/images/doodle-shooting.png'
    # Citation: the following two images are from https://www.amazon.com/Lima-Sky-LLC-Doodle-Jump/dp/B00CTXBO9M 
    leftDoodler = '../assets/images/doodle2.png'
    rightDoodler = '../assets/images/doodle1.png'
    monsterImage = '../assets/images/monster1.png'

class Sounds:
    # Ciation: sounds downloaded from https://www.sounds-resource.com/mobile/doodlejump/sound/1636/
    jumpSound = '../assets/sounds/jump.wav'
    breakingPlatformSound = '../assets/sounds/breaking-arcade.mp3'
    fallingSound = '../assets/sounds/falling-sound-arcade.mp3'
    trapSound = '../assets/sounds/trap.mp3'
    startSound = '../assets/sounds/start.wav'
    springSound = '../assets/sounds/trampoline.mp3'
    shootBulletSound = '../assets/sounds/pistol_shoot.mp3'
    grabPowerUpSound = '../assets/sounds/collect.mp3'


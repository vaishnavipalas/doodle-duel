class GameSettings:
    playerWidth = 40
    playerHeight = 40
    platformWidth = 50
    platformHeight = 15
    platformSpacing = 40
    gravity = 1
    jumpStrength = -15
    gameWidth = 400
    gameHeight = 600
    offset = gameWidth + 50

class Images:
    # images taken from https://doodlejump.io/
    platformImage = '../assets/images/doodle-platform.png'
    brokenPlatformImage = '../assets/images/broken-platform.png'
    platformWithSpring = '../assets/images/platform-w-spring.png'
    doodleShootingImage = '../assets/images/doodle-shooting.png'
    leftDoodler = '../assets/images/doodle2.png'
    rightDoodler = '../assets/images/doodle1.png'

class Sounds:
    # sounds downloaded from https://www.sounds-resource.com/mobile/doodlejump/sound/1636/
    jumpSound = '../assets/sounds/jump.wav'
    breakingPlatformSound = '../assets/sounds/breaking-arcade.mp3'
    fallingSound = '../assets/sounds/falling-sound-arcade.mp3'
    trapSound = '../assets/sounds/trap.mp3'
    startSound = '../assets/sounds/start.wav'
    springSound = '../assets/sounds/trampoline.mp3'
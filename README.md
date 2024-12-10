# Doodle Duel: 2-Player Version of Doodle Jump

## Description

Doodle Duel is a multiplayer adaptation of the classic game Doodle Jump. 
Players ascend endless platforms, collect power-ups, and avoid obstacles such as black holes and monsters. 
The game includes two multiplayer modes:

- Player vs. Player: Two players compete using keyboard controls.
- Player vs. AI: A human player competes against an AI opponent.

Players can customize their gameplay experience by selecting one of three unique themes (outer space, underwater, or default). 
The game ends when one player falls or collides with a hazard, and the winner is determined by the highest score.


## Run Instructions

Install Python 3.7+ on your system.
Install the required library cmu_graphics by running the following command in the terminal:

```bash
pip install cmu-graphics
```

Download [Doodle Jump font](https://2ttf.com/9L8ZEUpWnuu) by LimaSky.
Install the font on your system so it can be accessed by the game.


Download the project folder to your computer.
Open the folder in a Python-compatible IDE such as VS Code.
Navigate to the main script file (e.g., main.py) in your IDE.
Run the file by pressing IDE’s “Run” command (for VS Code it is Command+B).

Please keep all project files (assets and src) in their original folders. The game requires specific directory paths to load images and sounds.


## Shortcut Commands for Testing/Demo

Use the following keys during gameplay to test or demonstrate specific features:

- 'p' Key: Generates a power-up at the position (200, -20). This power-up will have the effect of a gravity inverter.
- 'm' Key: Generates a monster at the position (200, -20), which can be used to test monster interactions.
- 'o' Key: Sets the game over state for both players (first and second game), allowing you to simulate a game-over scenario.

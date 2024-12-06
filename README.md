# DS5100-Project
Monte Carlo Simulation Package
Metadata
Package Name: montecarlo_package
Version: 0.1
Author: Shelly Schwartz
Email: tfk6ua@virginia.edu
Description: A Python package for running Monte Carlo simulations with customizable dice, a game system, and a comprehensive results analyzer.
Dependencies: numpy, pandas
Synopsis
This package allows users to simulate games involving dice rolls and analyze the results with detailed statistical methods. Below is a step-by-step guide for using the package.

1. Die Class
The Die class allows users to create a single die object with customizable faces and weights. It includes functionality to roll the die and retrieve its state.

Example:
python
Copy code
from montecarlo_package.montecarlo import Die
import numpy as np

# Create a die with faces 1 to 6
die = Die(np.array([1, 2, 3, 4, 5, 6]))

# Change the weight of the face with value 3
die.change_weight(3, 5.0)

# Roll the die 10 times
results = die.roll(10)

# Get the current state of the die
state = die.get_state()
print(state)
2. Game Class
The Game class allows users to play a game using multiple dice. Results from multiple rolls can be stored in either a wide or narrow format.

Example:
python
Copy code
from montecarlo_package.montecarlo import Game, Die
import numpy as np

# Create two dice with different faces
die1 = Die(np.array([1, 2, 3]))
die2 = Die(np.array([4, 5, 6]))

# Initialize a game with the two dice
game = Game([die1, die2])

# Play the game with 10 rolls
game.play(10)

# Retrieve the results in wide format
wide_results = game.get_recent_play('wide')
print(wide_results)

# Retrieve the results in narrow format
narrow_results = game.get_recent_play('narrow')
print(narrow_results)
3. Analyzer Class
The Analyzer class provides tools to analyze the results of a game, including identifying jackpots, face counts, combinations, and permutations.

Example:
python
Copy code
from montecarlo_package.montecarlo import Analyzer

# Analyze the results of a game
analyzer = Analyzer(game)

# Count the number of jackpots
jackpots = analyzer.jackpot()
print(f"Number of jackpots: {jackpots}")

# Get face counts per roll
face_counts = analyzer.face_counts_per_roll()
print(face_counts)

# Get unique combinations (ignoring order)
combinations = analyzer.combo_count()
print(combinations)

# Get unique permutations (considering order)
permutations = analyzer.permutation_count()
print(permutations)
API Documentation
Die Class
Die(faces: np.ndarray)
Description: Initializes a die with unique faces and default weights.
Arguments:
faces: A numpy array of unique face symbols (numbers or strings).
Methods:
change_weight(face, new_weight)
Changes the weight of a specific face.
roll(num_rolls=1)
Rolls the die and returns the results.
get_state()
Returns the current state of the die as a DataFrame.
Game Class
Game(dice: list)
Description: Initializes a game with multiple dice.
Arguments:
dice: A list of Die objects.
Methods:
play(num_rolls)
Rolls all dice a specified number of times.
get_recent_play(form='wide')
Retrieves the results of the most recent game in the specified format ('wide' or 'narrow').
Analyzer Class
Analyzer(game: Game)
Description: Analyzes the results of a game.
Arguments:
game: A Game object to analyze.
Methods:
jackpot()
Counts the number of rolls where all dice show the same face.
face_counts_per_roll()
Counts the occurrences of each face in each roll.
combo_count()
Calculates unique combinations of dice faces (ignoring order).
permutation_count()
Calculates unique permutations of dice faces (considering order).
Installation
Clone the repository:
bash
Copy code
git clone <repository-link>
cd <repository-folder>
Install the package in editable mode:
bash
Copy code
pip install -e .
Tests
Unit tests are available in the tests folder. To run the tests:

bash
Copy code
python -m unittest discover -s tests

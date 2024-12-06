import numpy as np
import pandas as pd


class Die:
    """
    represents a single die, allowing for customizable faces and weights
    """

    def __init__(self, faces):
        """
        sets up a die with the given faces and default weights for each face.
        the weights are set to 1.0 initially.

        arguments:
            faces: a numpy array containing unique face symbols, which can be numbers or strings

        errors:
            raises typeerror if the faces input is not a numpy array
            raises valueerror if there are duplicate face values
        """
        if not isinstance(faces, np.ndarray):
            raise TypeError("faces must be provided as a numpy array")

        if len(set(faces)) != len(faces):
            raise ValueError("all faces must be unique")

        self.faces = faces
        self.weights = np.ones(len(faces), dtype=float)
        # create a dataframe to store faces and their weights
        self.die_state = pd.DataFrame({'Faces': self.faces, 'Weights': self.weights})
        self.die_state.set_index('Faces', inplace=True)

    def change_weight(self, face, new_weight):
        """
        updates the weight of a specified face.

        arguments:
            face: the face whose weight is being updated
            new_weight: the new weight value, which should be numeric (int or float)

        errors:
            raises indexerror if the face is not part of the die
            raises typeerror if the weight is not a valid numeric type
        """
        if face not in self.die_state.index:
            raise IndexError("the face does not exist in this die")

        try:
            new_weight = float(new_weight)
        except ValueError:
            raise TypeError("weight must be a number")

        # assign the new weight to the specified face
        self.die_state.loc[face, 'Weights'] = new_weight

    def roll(self, num_rolls=1):
        """
        rolls the die the specified number of times and returns the results.

        arguments:
            num_rolls: how many times to roll the die. defaults to 1.

        returns:
            a list of face values based on the roll results
        """
        outcomes = self.die_state.sample(
            n=num_rolls,
            weights=self.die_state['Weights'],
            replace=True
        )
        return list(outcomes.index)

    def get_state(self):
        """
        shows the current state of the die, including faces and weights

        returns:
            a dataframe copy with faces and their associated weights
        """
        return self.die_state.copy()



class Game:
    """
    handles rolling multiple dice together, simulating a game
    """

    def __init__(self, dice):
        """
        sets up the game with a collection of dice

        arguments:
            dice: a list containing multiple die objects
        """
        self.dice = dice
        self.results = None

    def play(self, num_rolls):
        """
        rolls all dice in the game a specified number of times

        arguments:
            num_rolls: how many times each die should be rolled

        stores:
            the results in a private dataframe in wide format, where rows
            represent roll numbers and columns represent dice
        """
        roll_results = {}
        for i, die in enumerate(self.dice):
            roll_results[i] = die.roll(num_rolls)
        self.results = pd.DataFrame(roll_results)

    def get_recent_play(self, form='wide'):
        """
        retrieves the results of the most recent play

        arguments:
            form: the format of the output, either 'wide' (default) or 'narrow'

        returns:
            a dataframe in the specified format

        errors:
            raises valueerror if the requested format is not valid
        """
        if self.results is None:
            raise ValueError("no results to show. play the game first")

        if form == 'wide':
            return self.results.copy()
        elif form == 'narrow':
            narrow_results = self.results.melt(var_name='Die', value_name='Outcome')
            return narrow_results
        else:
            raise ValueError("invalid format. use 'wide' or 'narrow'")


class Analyzer:
    """
    provides tools for analyzing the results of a game
    """

    def __init__(self, game):
        """
        links the analyzer to a game and fetches its results

        arguments:
            game: a game object to analyze

        errors:
            raises valueerror if the input is not a game object
            raises valueerror if the game has no results to analyze
        """
        if not isinstance(game, Game):
            raise ValueError("input must be a game object")
        if game.results is None:
            raise ValueError("the game has no results to analyze")

        self.results = game.get_recent_play()

    def jackpot(self):
        """
        counts how many rolls have all dice showing the same face

        returns:
            an integer representing the number of jackpots
        """
        jackpots = 0
        for _, row in self.results.iterrows():
            if len(set(row)) == 1:
                jackpots += 1
        return jackpots

    def face_counts_per_roll(self):
        """
        calculates how often each face appears in each roll

        returns:
            a dataframe where rows are roll numbers and columns are face counts
        """
        counts = self.results.apply(pd.Series.value_counts, axis=1).fillna(0)
        return counts

    def combo_count(self):
        """
        calculates unique combinations of faces rolled, ignoring order

        returns:
            a dataframe with combinations and their frequencies
        """
        combinations = self.results.apply(lambda row: tuple(sorted(row)), axis=1)
        combo_counts = combinations.value_counts()
        combo_df = pd.DataFrame({'Combination': combo_counts.index, 'Frequency': combo_counts.values})
        return combo_df

    def permutation_count(self):
        """
        calculates unique permutations of faces rolled, considering order

        returns:
            a dataframe with permutations and their frequencies
        """
        permutations = self.results.apply(tuple, axis=1)
        permutation_counts = permutations.value_counts()
        permutation_df = pd.DataFrame({'Permutation': permutation_counts.index, 'Frequency': permutation_counts.values})
        return permutation_df

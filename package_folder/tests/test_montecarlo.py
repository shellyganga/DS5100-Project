import unittest
import numpy as np
import pandas as pd
from package.montecarlo import Die, Analyzer, Game

class TestDie(unittest.TestCase):
    """
    tests for the die class
    """

    def setUp(self):
        # create a die with faces 1 to 6
        self.die = Die(np.array([1, 2, 3, 4, 5, 6]))

    def test_init(self):
        # test that the die is initialized correctly
        self.assertEqual(len(self.die.faces), 6)
        self.assertTrue(all(weight == 1.0 for weight in self.die.weights))
        # test error when duplicate faces are provided
        with self.assertRaises(ValueError):
            Die(np.array([1, 2, 2, 3]))

    def test_change_weight(self):
        # test changing the weight of a face
        self.die.change_weight(3, 5.0)
        self.assertEqual(self.die.die_state.loc[3, 'Weights'], 5.0)
        # test another face
        self.die.change_weight(1, 2.0)
        self.assertEqual(self.die.die_state.loc[1, 'Weights'], 2.0)
        # test invalid face
        with self.assertRaises(IndexError):
            self.die.change_weight(7, 2.0)
        # test invalid weight type
        with self.assertRaises(TypeError):
            self.die.change_weight(3, "invalid")

    def test_roll(self):
        # test rolling the die
        rolls = self.die.roll(10)
        self.assertEqual(len(rolls), 10)
        self.assertTrue(all(face in self.die.faces for face in rolls))
        # make one face heavily weighted and test rolls
        self.die.change_weight(6, 10)
        weighted_rolls = self.die.roll(100)
        self.assertGreater(weighted_rolls.count(6), 50)  # most rolls should be 6

    def test_get_state(self):
        # test getting the current state of the die
        state = self.die.get_state()
        self.assertIsInstance(state, pd.DataFrame)
        self.assertEqual(len(state), 6)


class TestGame(unittest.TestCase):
    """
    tests for the game class
    """

    def setUp(self):
        # create a game with two dice
        die1 = Die(np.array([1, 2, 3]))
        die2 = Die(np.array([4, 5, 6]))
        self.game = Game([die1, die2])

    def test_init(self):
        # test that the game initializes correctly with dice
        self.assertEqual(len(self.game.dice), 2)

    def test_play(self):
        # test playing the game
        self.game.play(10)
        self.assertEqual(len(self.game.results), 10)
        # validate specific outcomes
        die1 = Die(np.array([1, 2]))
        die1.change_weight(2, 5)
        game = Game([die1])
        game.play(20)
        results = game.get_recent_play('wide')
        self.assertGreater(len(results[0][results[0] == 2]), 10)  # more rolls should show face 2

    def test_get_recent_play(self):
        # test getting play results in wide format
        self.game.play(5)
        wide_results = self.game.get_recent_play('wide')
        self.assertIsInstance(wide_results, pd.DataFrame)
        self.assertEqual(wide_results.shape[0], 5)
        # test narrow format
        narrow_results = self.game.get_recent_play('narrow')
        self.assertIsInstance(narrow_results, pd.DataFrame)
        self.assertGreater(narrow_results.shape[0], 5)
        # test invalid format
        with self.assertRaises(ValueError):
            self.game.get_recent_play('invalid')


class TestAnalyzer(unittest.TestCase):
    """
    tests for the analyzer class
    """

    def setUp(self):
        # create a game and analyzer
        die1 = Die(np.array([1, 2, 3]))
        die2 = Die(np.array([1, 2, 3]))
        game = Game([die1, die2])
        game.play(10)
        self.analyzer = Analyzer(game)

    def test_init(self):
        # test analyzer initialization
        self.assertIsInstance(self.analyzer.results, pd.DataFrame)
        self.assertEqual(len(self.analyzer.results), 10)
        # test invalid initialization
        with self.assertRaises(ValueError):
            Analyzer("invalid_game")

    def test_jackpot(self):
        mock_results = pd.DataFrame({
            0: [1, 1, 1, 1, 1],  # Die 1 results
            1: [1, 1, 1, 1, 1],  # Die 2 results
        })
        self.analyzer.results = mock_results  # Override self.results

        # Expected jackpot count
        expected_jackpots = 5

        # Call the jackpot method and verify the result
        actual_jackpots = self.analyzer.jackpot()

        self.assertEqual(actual_jackpots, expected_jackpots)

    def test_face_counts_per_roll(self):
        counts = self.analyzer.face_counts_per_roll()
        self.assertIsInstance(counts, pd.DataFrame)
        self.assertEqual(counts.shape[0], 10)  # 10 rolls
        # test specific face counts
        self.assertTrue((counts.sum(axis=1) == 2).all())  # each roll involves 2 dice

    def test_combo_count(self):
        # Mock deterministic game results
        mock_results = pd.DataFrame({
            0: [1, 1, 2, 3, 2],  # Die 1 results
            1: [1, 2, 2, 3, 3],  # Die 2 results
        })
        self.analyzer.results = mock_results  # Override self.results

        # Expected combinations (ignoring order)
        expected_combos = {
            (1, 1): 1,  # Appears once
            (1, 2): 1,
            (2, 2): 1,
            (3, 3): 1,
            (2, 3): 1,
        }

        combos = self.analyzer.combo_count()

        for combo, freq in expected_combos.items():
            self.assertIn(combo, combos['Combination'].tolist())
            self.assertEqual(
                combos.loc[combos['Combination'] == combo, 'Frequency'].values[0],
                freq
            )

        # Ensure no unexpected combinations are present
        actual_combos = set(combos['Combination'].tolist())
        self.assertEqual(set(expected_combos.keys()), actual_combos)

    def test_permutation_count(self):

        # Mock deterministic game results
        mock_results = pd.DataFrame({
            0: [1, 1, 2, 3, 2],  # Die 1 results
            1: [1, 2, 2, 3, 3],  # Die 2 results
        })
        self.analyzer.results = mock_results  # Override self.results

        # Expected permutations (considering order)
        expected_permutations = {
            (1, 1): 1,  # Appears once
            (1, 2): 1,
            (2, 2): 1,
            (3, 3): 1,
            (2, 3): 1,
        }

        permutations = self.analyzer.permutation_count()

        for perm, freq in expected_permutations.items():
            self.assertIn(perm, permutations['Permutation'].tolist())
            self.assertEqual(
                permutations.loc[permutations['Permutation'] == perm, 'Frequency'].values[0],
                freq
            )

        # Ensure no unexpected permutations are present
        actual_permutations = set(permutations['Permutation'].tolist())
        self.assertEqual(set(expected_permutations.keys()), actual_permutations)


if __name__ == '__main__':
    unittest.main()
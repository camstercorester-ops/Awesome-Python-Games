import unittest
from Code.Rock_Paper_Scissors_Spock_Lizard import name_to_number


class TestNameToNumber(unittest.TestCase):
    def test_valid_moves(self):
        # Test all valid moves
        self.assertEqual(name_to_number("rock"), 0)
        self.assertEqual(name_to_number("Spock"), 1)
        self.assertEqual(name_to_number("paper"), 2)
        self.assertEqual(name_to_number("lizard"), 3)
        self.assertEqual(name_to_number("scissors"), 4)

    def test_invalid_move(self):
        # Test invalid move
        with self.assertRaises(ValueError) as context:
            name_to_number("invalid")
        self.assertIn("is not a valid move", str(context.exception))

    def test_case_sensitivity(self):
        # Test that the function is case-sensitive
        with self.assertRaises(ValueError):
            name_to_number("Rock")
        with self.assertRaises(ValueError):
            name_to_number("spock")

    def test_non_string_input(self):
        # Test non-string inputs
        with self.assertRaises(ValueError) as context:
            name_to_number(123)
        self.assertIn("Input must be a string", str(context.exception))
        with self.assertRaises(ValueError):
            name_to_number(None)
        with self.assertRaises(ValueError):
            name_to_number(["rock"])

    def test_empty_string(self):
        # Test empty string input
        with self.assertRaises(ValueError):
            name_to_number("")

    def test_whitespace_string(self):
        # Test string with only whitespace
        with self.assertRaises(ValueError):
            name_to_number("   ")

if __name__ == '__main__':
    unittest.main()

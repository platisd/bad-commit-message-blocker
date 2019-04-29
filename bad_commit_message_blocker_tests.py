# Python code to demonstrate working of unittest
import unittest
import bad_commit_message_blocker as blocker


class TestCommitMessageBlocker(unittest.TestCase):

    def setUp(self):
        pass

    def test_checkSubjectUsesImperative_WhenImperative_WillReturnTrue(self):
        test_input = ["Refactor subsystem X for readability",
                      "Update getting started documentation",
                      "Remove deprecated methods",
                      "Release version 1.0.0",
                      "Add cool method to class"]
        for input in test_input:
            self.assertTrue(blocker.check_subject_uses_imperative(
                input), "\"" + input + "\" did not produce the expected result")

    def test_checkSubjectUsesImperative_WhenThirdPerson_WillReturnFalse(self):
        test_input = ["Refactors subsystem X for readability",
                      "Updates getting started documentation",
                      "Removes deprecated methods",
                      "Releases version 1.0.0",
                      "Adds cool method to class"]
        for input in test_input:
            self.assertFalse(blocker.check_subject_uses_imperative(
                input), "\"" + input + "\" did not produce the expected result")

    def test_checkSubjectUsesImperative_WhenPresentContinuous_WillReturnFalse(self):
        test_input = ["Refactoring subsystem X for readability",
                      "Updating getting started documentation",
                      "Removing deprecated methods",
                      "Releasing version 1.0.0",
                      "Adding cool method to class"]
        for input in test_input:
            self.assertFalse(blocker.check_subject_uses_imperative(
                input), "\"" + input + "\" did not produce the expected result")

    def test_checkSubjectUsesImperative_WhenSimplePast_WillReturnFalse(self):
        test_input = ["Refactored subsystem X for readability",
                      "Updated getting started documentation",
                      "Removed deprecated methods",
                      "Released version 1.0.0",
                      "Added cool method to class"]
        for input in test_input:
            self.assertFalse(blocker.check_subject_uses_imperative(
                input), "\"" + input + "\" did not produce the expected result")

    def test_checkSubjectUsesImperative_WhenRandom_WillReturnFalse(self):
        test_input = ["Documentation is updated",
                      "Addition of new class"]
        for input in test_input:
            self.assertFalse(blocker.check_subject_uses_imperative(
                input), "\"" + input + "\" did not produce the expected result")


if __name__ == '__main__':
    unittest.main()

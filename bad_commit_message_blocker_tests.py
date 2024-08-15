"""
A set of unit tests for the Bad Commit Message Blocker.

The most interesting (and prone to fail) part is the imperative mood rule.
This is why most tests are focused a round it. If you want to introduce
improvements/changes to the script, make sure that there are no regressions
and your newly introduced change is also covered by unit tests.
"""

import unittest
import bad_commit_message_blocker as blocker


class TestCommitMessageBlocker(unittest.TestCase):

    def setUp(self):
        pass

    def test_checkSubjectUsesImperative_WhenImperative_WillReturnTrue(self):
        test_input = [
            "Refactor subsystem X for readability",
            "Update getting started documentation",
            "Remove deprecated methods",
            "Release version 1.0.0",
            "Add cool method to class",
        ]
        for input in test_input:
            self.assertTrue(
                blocker.check_subject_uses_imperative(input),
                '"' + input + '" did not produce the expected result',
            )

    def test_checkSubjectUsesImperative_WhenThirdPerson_WillReturnFalse(self):
        test_input = [
            "Refactors subsystem X for readability",
            "Updates getting started documentation",
            "Removes deprecated methods",
            "Releases version 1.0.0",
            "Adds cool method to class",
        ]
        for input in test_input:
            self.assertFalse(
                blocker.check_subject_uses_imperative(input),
                '"' + input + '" did not produce the expected result',
            )

    def test_checkSubjectUsesImperative_WhenPresentContinuous_WillReturnFalse(self):
        test_input = [
            "Refactoring subsystem X for readability",
            "Updating getting started documentation",
            "Removing deprecated methods",
            "Releasing version 1.0.0",
            "Adding cool method to class",
        ]
        for input in test_input:
            self.assertFalse(
                blocker.check_subject_uses_imperative(input),
                '"' + input + '" did not produce the expected result',
            )

    def test_checkSubjectUsesImperative_WhenSimplePast_WillReturnFalse(self):
        test_input = [
            "Refactored subsystem X for readability",
            "Updated getting started documentation",
            "Removed deprecated methods",
            "Released version 1.0.0",
            "Added cool method to class",
        ]
        for input in test_input:
            self.assertFalse(
                blocker.check_subject_uses_imperative(input),
                '"' + input + '" did not produce the expected result',
            )

    def test_checkSubjectUsesImperative_WhenRandom_WillReturnFalse(self):
        test_input = ["Documentation is updated", "Addition of new class"]
        for input in test_input:
            self.assertFalse(
                blocker.check_subject_uses_imperative(input),
                '"' + input + '" did not produce the expected result',
            )

    def test_checkSubjectSeparateFromBody_WhenLineBetweenBodyAndSubject_WillReturnTrue(
        self,
    ):
        test_input = """Add this cool feature

        This cool feature is implemented because X and Y."""
        self.assertTrue(blocker.check_subject_is_separated_from_body(test_input))

    def test_checkSubjectSeparateFromBody_WhenNoLineBetweenBodyAndSubject_WillReturnFalse(
        self,
    ):
        test_input = """Add this cool feature
        This cool feature is implemented because X and Y."""
        self.assertFalse(blocker.check_subject_is_separated_from_body(test_input))

    def test_checkSubjectNotTooLong_WhenSubjectTooLong_WillReturnFalse(self):
        test_input = "This is a very very very, really long, humongous subject for a commit message"
        self.assertFalse(blocker.check_subject_is_not_too_long(test_input, 60))

    def test_checkSubjectTooLong_WhenSubjectNotTooLong_WillReturnTrue(self):
        test_input = "Add this neat commit message"
        self.assertTrue(blocker.check_subject_is_not_too_long(test_input, 60))

    def test_checkSubjectIsCapitalized_WhenSubjectBeginsWithCapital_WillReturnTrue(
        self,
    ):
        test_input = "Add this cool new feature"
        self.assertTrue(blocker.check_subject_is_capitalized(test_input))

    def test_checkSubjectIsCapitalized_WhenSubjectBeginsWithLower_WillReturnFalse(self):
        test_input = "add this weird-looking commit message"
        self.assertFalse(blocker.check_subject_is_capitalized(test_input))

    def test_checkSubjectDoesNotEndWithPeriod_WhenSubjectEndsWithPeriod_WillReturnFalse(
        self,
    ):
        test_input = "I am a strange person and do such things."
        self.assertFalse(blocker.check_subject_does_not_end_with_period(test_input))

    def test_checkSubjectDoesNotEndWithPeriod_WhenSubjectEndsWithoutPeriod_WillReturnTrue(
        self,
    ):
        test_input = "I am a strange person and don't end commit messages with a period"
        self.assertTrue(blocker.check_subject_does_not_end_with_period(test_input))

    def test_checkBodyLinesAreNotTooLong_WhenLinesTooLong_WillReturnFalse(self):
        test_input = """Add this cool new feature

        But damn...
        I feel like adding some pretty huge lines and forget to insert \\n's. This is just sad!"""
        self.assertFalse(blocker.check_body_lines_are_not_too_long(test_input, 72))

    def test_checkBodyLinesAreNotTooLong_WhenLinesNotTooLong_WillReturnTrue(self):
        test_input = """Add this cool new feature

        And nicely explain why it was added."""
        self.assertTrue(blocker.check_body_lines_are_not_too_long(test_input, 72))

    def test_checkBodyExplainsWhatAndWhy_WhenCalled_WillReturnTrue(self):
        # We cannot currently check this, so we always return true
        # along with a relevant printed out message
        test_input = "Something that does not matter"
        self.assertTrue(blocker.check_body_explains_what_and_why(test_input))

    def test_stripPrefix_WhenColonInMessage_WillReturnEverythingAfterColon(self):
        test_input = "feat: add new feature"
        expected_output = "add new feature"
        self.assertEqual(blocker.strip_prefix(test_input), expected_output)

    def test_stripPrefix_WhenNoColonInMessage_WillReturnWholeMessage(self):
        test_input = "add new feature"
        expected_output = "add new feature"
        self.assertEqual(blocker.strip_prefix(test_input), expected_output)


if __name__ == "__main__":
    unittest.main()

'''
The `bad commit message blocker` intends to inhibit commits with bad
messages from getting merged into a project.

It tries to enforce the "seven rules of a great Git commit message"
as described by Chris Beams here: https://chris.beams.io/posts/git-commit/.

The most challenging rule to implement, is (#5) using imperative mood
in the subject line. It works mostly as intended, but does not have 100%
accuracy, as it can generate false positive or false negative results
primarily due to programming-related terminology. This innaccuracy stems
from limitations of the (default) NLP parser the NLTK library utilizes.

The final rule (#7) about explaining what and why instead of how in the
body of a commit message, very subjective and therefore is left up to
the code reviewer to ensure it is being adhered to.
'''
import argparse
import sys
from textblob import TextBlob

DEFAULT_SUBJECT_LIMIT = 50
DEFAULT_BODY_LIMIT = 72


class CliColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def check_subject_is_separated_from_body(commit_message):
    lines = commit_message.splitlines()
    if len(lines) > 1:
        # The second line should be empty
        check_result = not lines[1]
    else:
        # If there is just one line then this rule doesn't apply
        check_result = True
    print_result(check_result, "Separate subject from body with a blank line")

    return check_result


def check_subject_is_not_too_long(commit_message, subject_limit):
    lines = commit_message.splitlines()
    check_result = len(lines[0]) <= subject_limit
    print_result(check_result, "Limit the subject line to " +
                 str(subject_limit) + " characters")

    return check_result


def check_subject_is_capitalized(commit_message):
    lines = commit_message.splitlines()
    # Check if first character is in upper case
    check_result = lines[0][0].isupper()
    print_result(check_result, "Capitalize the subject line")

    return check_result


def check_subject_does_not_end_with_period(commit_message):
    lines = commit_message.splitlines()
    check_result = not lines[0].endswith(".")
    print_result(check_result, "Do not end the subject line with a period")

    return check_result


def check_subject_uses_imperative(commit_message):
    first_line = commit_message.splitlines()[0]
    third_person_singular_present_verb = "VBZ"
    non_third_person_singular_present_verb = "VBP"
    # The default NLTK parser is not very good with imperative sentences
    # so we prefix the commit message with a personal pronoun so to
    # help it determine easier whether the upcoming word is a verb
    # and not a noun.
    # We will prefix in two different ways, so to avoid false results.
    # Read more here: https://stackoverflow.com/a/30823202/6485320
    # and here: https://stackoverflow.com/a/9572724/6485320
    third_person_prefix = "It "
    words_in_third_person_prefix_blob = len(third_person_prefix.split())
    non_third_person_prefix = "You "
    words_in_non_third_person_prefix_blob = len(
        non_third_person_prefix.split())
    # Turn the first character into a lowercase so to make it easier for
    # the parser to determine whether the word is a verb and its tense
    first_character_in_lowercase = first_line[0].lower()
    first_line = first_character_in_lowercase + first_line[1:]
    third_person_blob = TextBlob(third_person_prefix + first_line)
    non_third_person_blob = TextBlob(non_third_person_prefix + first_line)

    first_word, third_person_result = third_person_blob.tags[words_in_third_person_prefix_blob]
    _, non_third_person_result = non_third_person_blob.tags[words_in_non_third_person_prefix_blob]

    # We need to determine whether the first word is a non-third person verb
    # when parsed in a non-third person blob. However, there were some
    # false positives so we use a third person blob to ensure it is not a
    # third person verb. Unfortunately, there were now some false negatives
    # due to verbs in a non-third person form, being classified as being in
    # third person, when parsed in the third person blob.
    # So, we ultimately check if the verb ends with an 's' which is a pretty
    # good indicator of a third person, simple present tense verb.
    check_result = non_third_person_result == non_third_person_singular_present_verb and (
        third_person_result != third_person_singular_present_verb or not first_word.endswith("s"))
    print_result(check_result, "Use the imperative mood in the subject line")

    return check_result


def check_body_lines_are_not_too_long(commit_message, body_limit):
    lines = commit_message.splitlines()
    check_result = True
    for line in lines:
        if len(line) > body_limit:
            check_result = False
            break
    print_result(check_result, "Wrap the body at " +
                 str(body_limit) + " characters")

    return check_result


def check_body_explains_what_and_why(commit_message):
    what_vs_how_rule = "Use the body to explain what and why vs. how"
    print("[" + CliColors.OKBLUE + "  NA  " +
          CliColors.ENDC + "] " + what_vs_how_rule)

    return True


def print_result(check_passed, rule):
    print("[" + (CliColors.OKGREEN +
                 "PASSED" if check_passed else CliColors.FAIL + "FAILED") + CliColors.ENDC + "] " + rule)


def check(commit_message, subject_limit=DEFAULT_SUBJECT_LIMIT, body_limit=DEFAULT_BODY_LIMIT):
    all_rules_verified = check_subject_is_separated_from_body(
        commit_message)
    all_rules_verified &= check_subject_is_not_too_long(
        commit_message, subject_limit)
    all_rules_verified &= check_subject_is_capitalized(commit_message)
    all_rules_verified &= check_subject_does_not_end_with_period(
        commit_message)
    all_rules_verified &= check_subject_uses_imperative(commit_message)
    all_rules_verified &= check_body_lines_are_not_too_long(
        commit_message, body_limit)
    all_rules_verified &= check_body_explains_what_and_why(commit_message)

    return all_rules_verified


def main():
    parser_description = "Bad commit message blocker: Avoid bad commit messages in your repository"
    parser = argparse.ArgumentParser(description=parser_description)
    parser.add_argument("--message",
                        help="The commit message to check",
                        required=True)
    parser.add_argument("--subject-limit",
                        help="The maximum allowed length for a commit subject",
                        default=DEFAULT_SUBJECT_LIMIT)
    parser.add_argument("--body-limit",
                        help="The maximum allowed length for a line in the commit body",
                        default=DEFAULT_BODY_LIMIT)
    args = parser.parse_args()

    commit_message = args.message.strip()
    print(CliColors.HEADER + CliColors.BOLD +
          "Your commit message: " + CliColors.ENDC)
    print("===========================")
    print(commit_message)
    print("===========================")
    print(CliColors.HEADER + CliColors.BOLD +
          "Conformance to the 7 rules of a great Git commit message:" + CliColors.ENDC)

    all_rules_verified = check(commit_message, int(
        args.subject_limit), int(args.body_limit))

    sys.exit(0 if all_rules_verified else 1)


if __name__ == "__main__":
    main()

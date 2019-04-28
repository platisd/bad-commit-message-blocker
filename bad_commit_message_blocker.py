import argparse
import sys
from textblob import TextBlob


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
    # The default NLTK parser is not very good with imperative sentences
    # so we prefix the commit message with a personal pronoun so to
    # help it determine easier whether the upcoming word is a verb
    # and not a noun.
    # We will prefix in two different ways, so to avoid false results
    third_person_pronoun = "It "
    non_third_person_pronoun = "They "
    # Turn the first character into a lowercase so to make it easier for
    # the parser to determine whether the word is a verb and its tense
    first_character_in_lowercase = commit_message[0].lower()
    commit_message = first_character_in_lowercase + commit_message[1:]
    third_person_blob = TextBlob(third_person_pronoun + commit_message)
    non_third_person_blob = TextBlob(non_third_person_pronoun + commit_message)

    _, third_person_result = third_person_blob.tags[1]
    _, non_third_person_result = non_third_person_blob.tags[1]
    check_result = non_third_person_result == "VBP" and third_person_result != "VBZ"
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


def main():
    parser_description = "Bad commit message blocker: Avoid bad commit messages in your repository"
    parser = argparse.ArgumentParser(description=parser_description)
    parser.add_argument("--message",
                        help="The commit message to check",
                        required=True)
    parser.add_argument("--subject-limit",
                        help="The maximum allowed length for a commit subject",
                        default=50)
    parser.add_argument("--body-limit",
                        help="The maximum allowed length for a line in the commit body",
                        default=72)
    args = parser.parse_args()

    commit_message = args.message.strip()

    print(CliColors.HEADER + CliColors.BOLD +
          "Conformance to the 7 rules of a great Git commit message:" + CliColors.ENDC)

    all_rules_verified = check_subject_is_separated_from_body(commit_message)
    all_rules_verified &= check_subject_is_not_too_long(
        commit_message, int(args.subject_limit))
    all_rules_verified &= check_subject_is_capitalized(commit_message)
    all_rules_verified &= check_subject_does_not_end_with_period(
        commit_message)
    all_rules_verified &= check_subject_uses_imperative(commit_message)
    all_rules_verified &= check_body_lines_are_not_too_long(
        commit_message, int(args.body_limit))
    all_rules_verified &= check_body_explains_what_and_why(commit_message)

    sys.exit(0 if all_rules_verified else 1)


if __name__ == "__main__":
    main()

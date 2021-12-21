# Bad Commit Message Blocker [![Build Status](https://travis-ci.org/platisd/bad-commit-message-blocker.svg?branch=master)](https://travis-ci.org/platisd/bad-commit-message-blocker)
A simple script, doing some natural language processing, to inhibit
*git commits* with *bad messages* from getting merged.

![screenshot](https://i.imgur.com/B52Qxo7.png)

## What?
A Python3 script, easy to integrate with various CI machinery
(e.g. see [GitHub Actions example](#github-action))
that is meant to keep bad commit messages out of a project. It verifies
whether the [seven rules of a great Git commit message](https://chris.beams.io/posts/git-commit/)
by Chris Beams, are being followed:

1. Separate subject from body with a blank line
2. Limit the subject line to 50 characters
3. Capitalize the subject line
4. Do not end the subject line with a period
5. Use the imperative mood in the subject line
6. Wrap the body at 72 characters
7. Use the body to explain what and why vs. how

## Why?
The more a project grows in contributors and size, the more important
the quality of its commit messages becomes.

It is ultimately hard to quantify what makes a *good* commit message.
However, we can easily determine automatically whether it adheres to
most of the git commit message best practices. Having a script to
automatically verify that, aside of other rules that you might already
enforce (e.g. checking whether a task or a requirement is referenced)
can save a lot of time in the long run as well as even avoid conflicts
between the reviewer(s) and the reviewee.

After adopting this script, what you get is a set of best practices,
agreed upon by the project and automatically applied. This way,
everyone has to follow them or CI will not allow that commit in.
Simple as that! :innocent:

## How?
Most of the rules are trivial to implement in code, except two of them,
*no. 5* and *no. 7*. Specifically, checking whether the commit subject
begins with *imperative* mood is tricky due to limitations of the Natural
Language Processing libraries being utilized. You can read more about the
constraints [here](https://stackoverflow.com/a/9572724/6485320).
Essentially, it boils down to the lack of many imperative sentences
existing in the datasets used when training the relevant statistical
models. Subsequently, **the enforcement of this rule might produce some**
**false positive and false negative errors**.

On the other hand, verifying whether the commit body actually explains
*what* and *why* instead of *how* is not (?) possible, due to the
subjective nature of the problem.
All in all, in most cases, this is all the reviewers would have to do
themselves *manually*, to ensure the quality of a commit message.

### Get started
You need to have Python3 installed and follow the steps bellow:
* Install [TextBlob](https://textblob.readthedocs.io/en/dev/)
  * `pip3 install --user textblob`
* Install NLTK corpora
  * `python3 -m textblob.download_corpora`
* Run the script to verify a commit message
  * `python3 bad_commit_message_blocker.py --message "Add a really cool feature"`
* To define your own maximum character limits, call the script with the
appropriate arguments:
  * `--subject-limit` (defaults to `50`) to set the subject line limit. E.g.:
    * `python3 bad_commit_message_blocker.py --subject-limit 80 --message "Add a really cool feature"`
  * `--body-limit` (defaults to `72`) to set the body line limit. E.g.:
    *  `python3 bad_commit_message_blocker.py --body-limit 120 --message "Add a really cool feature"`

## GitHub Action

Now you can use this script as part of your **GitHub Actions** CI pipeline.

An example configuration can be seen below:

```yaml
name: Commit messages

on: [pull_request]

jobs:
  check-commit-message:
    if: github.event.pull_request.user.type != 'Bot'  # a number of GitHub Apps that can send PRs don't have configurable commits
    runs-on: ubuntu-20.04
    steps:
      - name: Verify commit messages follow best practices in CI
        uses: platisd/bad-commit-message-blocker@master
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          # Optionally set the subject character limit (default `50`)
          subject_limit: 60
          # Optionally set the body character limit (default `72`)
          body_limit: 100
          # Optionally set the remote branch name to merge (default `master`)
          remote_branch: dev
```

#!/bin/bash
set -eu

commits_since_master=$(git rev-list HEAD ^origin/master)

while read -r commit_hash; do
    commit_message="$(git log --format=%B -n 1 $commit_hash)"
    python3 bad_commit_message_blocker.py --message "$commit_message"
done <<< "$commits_since_master"

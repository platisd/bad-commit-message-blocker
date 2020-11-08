#!/bin/bash
set -eu

script_dir="$(dirname "$0")"
cd $script_dir

eval git clone "https://${INPUT_GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git" ${GITHUB_REPOSITORY}
cd $GITHUB_REPOSITORY
eval git config remote.origin.fetch +refs/heads/*:refs/remotes/origin/*
eval git fetch --all
eval git checkout ${GITHUB_HEAD_REF:-$(basename ${GITHUB_REF})}

commits_since_master=$(git rev-list HEAD ^origin/${INPUT_REMOTE_BRANCH})

while read -r commit_hash; do
    commit_message="$(git log --format=%B -n 1 ${commit_hash})"
    python3 $script_dir/bad_commit_message_blocker.py \
        --message "${commit_message}" \
        --subject-limit "${INPUT_SUBJECT_LIMIT}" \
        --body-limit "${INPUT_BODY_LIMIT}"
done <<< "$commits_since_master"

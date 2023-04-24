#!/bin/bash

git pull && git reset --hard HEAD

# PULL REQUEST

git checkout master && git pull

# VERSION ACTUAL
# git tag -l 'v*' | sort -V | tail -n 1

# VERSION ACTUALIZADA
# git tag -l 'v*' | sort -V | tail -n 1 | sed 's/^v//' | while IFS=. read major minor patch; do printf "v%d.%d.%d" $major $minor $((patch + 1)); done

VERSION_ACTUALIZADA=$(git tag -l 'v*' | sort -V | tail -n 1 | sed 's/^v//' | while IFS=. read major minor patch; do printf "v%d.%d.%d" $major $minor $((patch + 1)); done)

git tag -a $VERSION_ACTUALIZADA -m "$VERSION_ACTUALIZADA"

git push origin $VERSION_ACTUALIZADA





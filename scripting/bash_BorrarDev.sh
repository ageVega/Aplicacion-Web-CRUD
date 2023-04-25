#!/bin/bash

git reset --hard HEAD && git pull

git checkout master && git pull

git branch -D dev

git push origin --delete dev

git checkout -b dev

git push -u origin dev

git checkout master
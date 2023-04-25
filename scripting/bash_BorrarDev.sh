#!/bin/bash

git checkout master

git branch -d dev

git branch -D dev

git push origin --delete dev

git checkout -b dev

git push -u origin dev

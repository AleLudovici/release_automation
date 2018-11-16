#! /bin/sh

set -e

git checkout master &&
git pull &&
git checkout release &&
git merge master &&
git push origin release
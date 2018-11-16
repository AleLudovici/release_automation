#! /bin/sh

set -e

function merge_master_to_release() {
	git checkout master &&
	git pull &&
	git checkout release &&
	git merge master
}

function build() {
	echo 'building...'
}

function push() {
	git push origin release
}

if output=$(git status --porcelain) && [ -z "$output" ]; then
  # Working directory clean
  merge_master_to_release
  build
  push
else 
  # Uncommitted changes
  echo 'You have uncommitted changes. Please commit them before releasing.'
fi



#! /bin/sh

set -e

release_json_file="$1"

function check_prerequisites() {
	if output=$(git status --porcelain) && [ -z "$output" ]; then
	  # Working directory clean
	  retval=0
	else 
	  # Uncommitted changes
	  echo 'You have uncommitted changes. Please commit them before releasing.'
	  retval=1
	fi

	return "$retval"
}

function merge_master_to_release() {
	git checkout master &&
	git pull &&
	git checkout release &&
	git merge master
}

function build() {
	echo 'Building project...'
	xcodebuild clean build \
	-project release\ automation.xcodeproj \
	-UseModernBuildSystem=NO \
	-sdk iphonesimulator \
	-destination "name=iPhone 8"
}

function push() {
	git push origin release
}

function draft_release() {
	echo 'Creating release draft'
}

check_prerequisites
retval=$?
if [ "$retval" == 0 ]; then
  merge_master_to_release
  build
  push
  draft_release
fi

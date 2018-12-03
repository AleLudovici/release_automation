#! /bin/sh

set -e

version=$( /usr/libexec/PlistBuddy -c 'Print CFBundleShortVersionString' release\ automation/Info.plist )

credentials_file="credentials.txt"
token=$(cat "$credentials_file")
debug=$1

function is_branch_clean() {
	if output=$(git status --porcelain) && [ -z "$output" ]; then
		true
	else
	  	echo 'You have uncommitted changes. Please commit them before releasing.'
	  	false
	fi
}

function is_json_valid() {
	if validation=$(echo "$release_json" | python -m json.tool  > /dev/null) && [ -z "$validation" ]; then
	  	true
	 else
	  	false
	 fi
}

function check_prerequisites() {
#	is_branch_clean
    true
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

function tag() {
    git tag "$version"
    git push origin "$version"
}

function draft_release() {
    python scripts/changelog.py "$version" "$token" "$debug"
}

if check_prerequisites; then
#	merge_master_to_release
#  	build
#  	push
#  	tag
  	draft_release
fi